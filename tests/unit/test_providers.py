import json
from types import SimpleNamespace

import pytest

from ai_math_study.ports.llm import LLMRequest
from ai_math_study.ports.llm import ProviderProfile
from ai_math_study.providers import (
    CallBudgetExhaustedError, DeepSeekProvider, DryRunProvider, FakeProvider, LocalOnlyError,
    LocalOnlyProvider, MissingAPIKeyError,
    ModelUnavailableError, OpenAIProvider, ReplayProvider,
    ResponseIncompleteError, ResponseRefusedError, ResponseSchemaError,
)
from ai_math_study.providers.fake import request_fingerprint


def request(model: str = "deepseek-v4-flash") -> LLMRequest:
    return LLMRequest(model, "final only", "input", "result", {
        "type": "object", "additionalProperties": False,
        "properties": {"ok": {"type": "boolean"}}, "required": ["ok"],
    })


class Responses:
    def __init__(self, response):
        self.response = response
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class ChatCompletions:
    def __init__(self, response):
        self.response = response
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        self.calls = getattr(self, "calls", []) + [kwargs]
        if isinstance(self.response, list):
            value = self.response.pop(0)
            if isinstance(value, Exception):
                raise value
            return value
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def test_openai_uses_responses_strict_schema_and_no_storage():
    responses = Responses(SimpleNamespace(
        output_text=json.dumps({"ok": True}), status="completed", model="gpt-5.6", id="r1",
    ))
    provider = OpenAIProvider(client=SimpleNamespace(responses=responses))
    assert provider.generate(request()).data == {"ok": True}
    assert responses.kwargs["store"] is False
    assert responses.kwargs["text"]["format"]["type"] == "json_schema"
    assert responses.kwargs["text"]["format"]["strict"] is True
    assert "previous_response_id" not in responses.kwargs


def test_openai_fails_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyError):
        OpenAIProvider().generate(request())


@pytest.mark.parametrize("response,error", [
    (SimpleNamespace(output_text="", status="incomplete"), ResponseIncompleteError),
    (SimpleNamespace(output_text="", status="completed", refusal="no"), ResponseRefusedError),
])
def test_openai_reports_incomplete_and_refusal(response, error):
    provider = OpenAIProvider(client=SimpleNamespace(responses=Responses(response)))
    with pytest.raises(error):
        provider.generate(request())


def test_model_unavailable_never_falls_back():
    provider = OpenAIProvider(client=SimpleNamespace(responses=Responses(Exception("model not found"))))
    with pytest.raises(ModelUnavailableError):
        provider.generate(request())


def ds_provider(chat, *, thinking=False, **kwargs):
    profile = ProviderProfile(
        provider="deepseek",
        model="deepseek-v4-pro" if thinking else "deepseek-v4-flash",
        thinking=thinking,
        reasoning_effort="high" if thinking else None,
    )
    return DeepSeekProvider(
        profile, client=SimpleNamespace(chat=SimpleNamespace(completions=chat)),
        sleep=lambda _: None, jitter=lambda _a, _b: 0, **kwargs,
    )


def response(content='{"ok": true}', finish="stop", model="deepseek-v4-flash"):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content), finish_reason=finish)],
        model=model, id="ds1",
    )


def test_deepseek_flash_explicitly_disables_thinking_and_validates_schema():
    chat = ChatCompletions(SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(content=json.dumps({"ok": True})),
            finish_reason="stop",
        )],
        model="deepseek-v4-flash", id="ds1",
    ))
    provider = ds_provider(chat)
    assert provider.generate(request()).data == {"ok": True}
    assert chat.kwargs["response_format"] == {"type": "json_object"}
    assert chat.kwargs["messages"][0]["role"] == "system"
    assert "json" in chat.kwargs["messages"][0]["content"].lower()
    assert chat.kwargs["extra_body"] == {"thinking": {"type": "disabled"}}
    assert "reasoning_effort" not in chat.kwargs


def test_deepseek_pro_explicitly_enables_thinking():
    chat = ChatCompletions(response(model="deepseek-v4-pro"))
    provider = ds_provider(chat, thinking=True)
    assert provider.generate(request("deepseek-v4-pro")).data == {"ok": True}
    assert chat.kwargs["extra_body"] == {"thinking": {"type": "enabled"}}
    assert chat.kwargs["reasoning_effort"] == "high"


def test_deepseek_fails_without_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyError):
        DeepSeekProvider(ProviderProfile("deepseek", "deepseek-v4-flash", False)).generate(request())


@pytest.mark.parametrize("finish_reason,error", [
    ("length", CallBudgetExhaustedError),
    ("content_filter", ResponseRefusedError),
])
def test_deepseek_reports_incomplete_and_refusal(finish_reason, error):
    chat = ChatCompletions(SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(content=""),
            finish_reason=finish_reason,
        )],
    ))
    provider = ds_provider(chat)
    with pytest.raises(error):
        provider.generate(request())


def test_deepseek_model_unavailable_never_falls_back():
    chat = ChatCompletions(Exception("model not found"))
    provider = ds_provider(chat)
    with pytest.raises(ModelUnavailableError):
        provider.generate(request())


def test_invalid_schema_response_consumes_same_three_call_budget():
    chat = ChatCompletions([response('{"ok": "yes"}') for _ in range(3)])
    provider = ds_provider(chat)
    with pytest.raises(CallBudgetExhaustedError) as caught:
        provider.generate(request())
    assert len(chat.calls) == 3
    assert isinstance(caught.value.__cause__, ResponseSchemaError)


def test_http_and_finish_regeneration_share_global_budget():
    retryable = Exception("busy")
    retryable.status_code = 429  # type: ignore[attr-defined]
    chat = ChatCompletions([retryable, response(finish="length"), response('{"ok": "bad"}')])
    provider = ds_provider(chat)
    with pytest.raises(CallBudgetExhaustedError):
        provider.generate(request())
    assert len(chat.calls) == 3


def test_non_retryable_http_never_spends_second_call():
    invalid = Exception("bad request")
    invalid.status_code = 400  # type: ignore[attr-defined]
    chat = ChatCompletions([invalid, response()])
    provider = ds_provider(chat)
    with pytest.raises(Exception, match="non-retryable"):
        provider.generate(request())
    assert len(chat.calls) == 1


def test_attempt_timeout_and_deadline_are_bounded():
    chat = ChatCompletions(response())
    provider = ds_provider(chat, deadline_seconds=180, attempt_timeout_seconds=55)
    provider.generate(request())
    assert 10 <= chat.kwargs["timeout"] <= 55


def test_telemetry_is_hashed_and_contains_no_prompt_body():
    class Sink:
        def __init__(self):
            self.events = []

        def record(self, event):
            self.events.append(event)

    sink = Sink()
    chat = ChatCompletions(response())
    profile = ProviderProfile("deepseek", "deepseek-v4-flash", False)
    provider = DeepSeekProvider(
        profile, client=SimpleNamespace(chat=SimpleNamespace(completions=chat)), telemetry=sink
    )
    private_request = request()
    private_request = LLMRequest(
        private_request.model, private_request.instructions, "PRIVATE-PROMPT-BODY",
        private_request.schema_name, private_request.json_schema,
    )
    provider.generate(private_request)
    event = sink.events[0]
    assert len(event.request_hash) == 64
    assert "PRIVATE-PROMPT-BODY" not in repr(event)
    assert event.attempt == 1
    assert event.error_code is None


def test_local_only_provider_has_no_client_or_network_path():
    provider = LocalOnlyProvider()
    assert not hasattr(provider, "_client")
    with pytest.raises(LocalOnlyError):
        provider.generate(request())


def test_fake_dry_run_and_replay_are_offline():
    req = request()
    assert FakeProvider([{"ok": True}]).generate(req).data["ok"] is True
    dry = DryRunProvider({"ok": False})
    assert dry.generate(req).response_id == "dry-run"
    replay = ReplayProvider({request_fingerprint(req): {"ok": True}})
    assert replay.generate(req).data == {"ok": True}
