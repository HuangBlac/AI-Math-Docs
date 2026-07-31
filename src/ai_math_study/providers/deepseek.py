from __future__ import annotations

import hashlib
import json
import os
import random
import time
from collections.abc import Callable
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from ai_math_study.ports.llm import (
    LLMCallTelemetry,
    LLMRequest,
    LLMResult,
    ProviderProfile,
    TelemetrySink,
)
from .errors import (
    CallBudgetExhaustedError,
    LLMProviderError,
    MissingAPIKeyError,
    ModelUnavailableError,
    ResponseIncompleteError,
    ResponseRefusedError,
    ResponseSchemaError,
)


_RETRYABLE_HTTP = {408, 429, 500, 502, 503, 504}
_NON_RETRYABLE_HTTP = {400, 401, 403, 404, 422}
_SUPPORTED_MODELS = {"deepseek-v4-flash", "deepseek-v4-pro"}


class DeepSeekProvider:
    """Capability-aware DeepSeek V4 Chat Completions adapter.

    All HTTP retries, truncated completions, empty/invalid JSON and schema
    regeneration share one deadline and one three-call budget.
    """

    BASE_URL = "https://api.deepseek.com"

    def __init__(
        self,
        profile: ProviderProfile,
        *,
        api_key: str | None = None,
        client: Any | None = None,
        max_calls: int = 3,
        deadline_seconds: float = 180,
        attempt_timeout_seconds: float = 55,
        telemetry: TelemetrySink | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        jitter: Callable[[float, float], float] = random.uniform,
    ) -> None:
        if profile.provider != "deepseek":
            raise ValueError("DeepSeekProvider requires a deepseek profile")
        if profile.model not in _SUPPORTED_MODELS:
            raise ModelUnavailableError(f"unsupported DeepSeek V4 model {profile.model!r}")
        if max_calls < 1 or max_calls > 3:
            raise ValueError("max_calls must be between 1 and 3")
        self.profile = profile
        self._api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self._client = client
        self._max_calls = max_calls
        self._deadline_seconds = deadline_seconds
        self._attempt_timeout_seconds = attempt_timeout_seconds
        self._telemetry = telemetry
        self._clock = clock
        self._sleep = sleep
        self._jitter = jitter

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self._api_key:
            raise MissingAPIKeyError("DEEPSEEK_API_KEY is required for DeepSeekProvider")
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise LLMProviderError("install the 'openai' package to use DeepSeekProvider") from exc
        self._client = OpenAI(api_key=self._api_key, base_url=self.BASE_URL)
        return self._client

    def generate(self, request: LLMRequest) -> LLMResult:
        if request.model != self.profile.model:
            raise ModelUnavailableError(
                f"request model {request.model!r} does not match profile {self.profile.model!r}"
            )
        try:
            validator = Draft202012Validator(request.json_schema)
            validator.check_schema(request.json_schema)
        except SchemaError as exc:
            raise ResponseSchemaError(f"invalid local JSON schema: {exc.message}") from exc

        start = self._clock()
        request_hash = hashlib.sha256(
            json.dumps(
                {
                    "model": request.model,
                    "instructions": request.instructions,
                    "input": request.input_text,
                    "schema": request.json_schema,
                },
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        last_error: LLMProviderError | None = None
        output_limit = request.max_output_tokens

        for attempt in range(1, self._max_calls + 1):
            if attempt > 1:
                cap = float(2 ** (attempt - 2))
                self._sleep(self._jitter(0.0, cap))
            elapsed = self._clock() - start
            remaining = self._deadline_seconds - elapsed
            future_backoff = 1.0 if attempt < self._max_calls else 0.0
            timeout = min(self._attempt_timeout_seconds, remaining - future_backoff - 5.0)
            if timeout < 10:
                raise CallBudgetExhaustedError("insufficient deadline for another DeepSeek call") from last_error

            call_start = self._clock()
            finish: str | None = None
            error_code: str | None = None
            response: Any | None = None
            try:
                response = self._get_client().chat.completions.create(
                    **self._payload(request, timeout, output_limit)
                )
                choice = (response.choices or [None])[0]
                if choice is None:
                    raise ResponseIncompleteError("response contained no choices")
                finish = getattr(choice, "finish_reason", None)
                if finish == "length":
                    output_limit = min((output_limit or 4096) * 2, 32768)
                    raise ResponseIncompleteError("response truncated; requesting a fresh generation")
                if finish not in (None, "stop"):
                    if finish in {"content_filter", "refusal"}:
                        raise ResponseRefusedError(f"finish_reason={finish}")
                    raise ResponseRefusedError(f"unknown finish_reason={finish}")
                content = getattr(choice.message, "content", None)
                if not content:
                    raise ResponseIncompleteError("response returned empty JSON content")
                try:
                    data = json.loads(content)
                except (TypeError, json.JSONDecodeError) as exc:
                    raise ResponseSchemaError("response was not valid JSON") from exc
                if not isinstance(data, dict):
                    raise ResponseSchemaError("structured output root must be an object")
                try:
                    validator.validate(data)
                except ValidationError as exc:
                    raise ResponseSchemaError(
                        f"structured output failed local schema validation: {exc.message}"
                    ) from exc
                self._record(request_hash, attempt, call_start, finish, None, response)
                return LLMResult(
                    data=data,
                    model=getattr(response, "model", request.model),
                    response_id=getattr(response, "id", None),
                )
            except ResponseRefusedError:
                self._record(request_hash, attempt, call_start, finish, "REFUSED", response)
                raise
            except (ResponseIncompleteError, ResponseSchemaError) as exc:
                last_error = exc
                error_code = type(exc).__name__
            except LLMProviderError:
                raise
            except Exception as exc:
                status = getattr(exc, "status_code", None)
                code = str(getattr(exc, "code", "") or "")
                message = str(exc).lower()
                error_code = code or (str(status) if status is not None else type(exc).__name__)
                if status == 404 or ("model" in message and "not found" in message):
                    self._record(request_hash, attempt, call_start, finish, error_code, response)
                    raise ModelUnavailableError(f"model {request.model!r} unavailable") from exc
                if status == 402:
                    self._record(request_hash, attempt, call_start, finish, "BUDGET_EXHAUSTED", response)
                    raise CallBudgetExhaustedError("DeepSeek account budget exhausted") from exc
                if status in _NON_RETRYABLE_HTTP:
                    self._record(request_hash, attempt, call_start, finish, error_code, response)
                    raise LLMProviderError(f"non-retryable DeepSeek HTTP {status}") from exc
                if status not in _RETRYABLE_HTTP and code != "insufficient_system_resource":
                    self._record(request_hash, attempt, call_start, finish, error_code, response)
                    raise LLMProviderError(f"unknown DeepSeek failure: {exc}") from exc
                last_error = LLMProviderError(f"retryable DeepSeek failure: {error_code}")
            self._record(request_hash, attempt, call_start, finish, error_code, response)

        assert last_error is not None
        raise CallBudgetExhaustedError(
            f"DeepSeek call budget exhausted after {self._max_calls} attempts"
        ) from last_error

    def _payload(
        self, request: LLMRequest, timeout: float, output_limit: int | None
    ) -> dict[str, Any]:
        schema = json.dumps(request.json_schema, ensure_ascii=False)
        payload: dict[str, Any] = {
            "model": self.profile.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        f"{request.instructions}\n\nReturn only JSON matching this JSON schema:\n{schema}"
                    ),
                },
                {"role": "user", "content": request.input_text},
            ],
            "response_format": {"type": "json_object"},
            "stream": False,
            "timeout": timeout,
            "extra_body": {
                "thinking": {"type": "enabled" if self.profile.thinking else "disabled"}
            },
        }
        if self.profile.thinking:
            payload["reasoning_effort"] = self.profile.reasoning_effort or "high"
        if output_limit is not None:
            payload["max_tokens"] = output_limit
        return payload

    def _record(
        self,
        request_hash: str,
        attempt: int,
        started: float,
        finish: str | None,
        error_code: str | None,
        response: Any | None,
    ) -> None:
        if self._telemetry is None:
            return
        usage = getattr(response, "usage", None)
        self._telemetry.record(
            LLMCallTelemetry(
                provider="deepseek",
                model=self.profile.model,
                thinking=self.profile.thinking,
                request_hash=request_hash,
                attempt=attempt,
                latency_ms=max(0, round((self._clock() - started) * 1000)),
                finish_reason=finish,
                error_code=error_code,
                input_tokens=getattr(usage, "prompt_tokens", None),
                output_tokens=getattr(usage, "completion_tokens", None),
            )
        )
