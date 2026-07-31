from __future__ import annotations

import hashlib
import json
from collections import deque
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from ai_math_study.ports.llm import LLMRequest, LLMResult
from .errors import LLMProviderError


def request_fingerprint(request: LLMRequest) -> str:
    value = {
        "model": request.model, "instructions": request.instructions,
        "input_text": request.input_text, "schema_name": request.schema_name,
        "json_schema": request.json_schema,
        "max_output_tokens": request.max_output_tokens,
    }
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class FakeProvider:
    """FIFO fake; values may be mappings, results, exceptions, or callables."""

    def __init__(self, responses: Iterable[Any] = ()) -> None:
        self.responses = deque(responses)
        self.requests: list[LLMRequest] = []

    def generate(self, request: LLMRequest) -> LLMResult:
        self.requests.append(request)
        if not self.responses:
            raise LLMProviderError("FakeProvider has no queued response")
        value = self.responses.popleft()
        if isinstance(value, BaseException):
            raise value
        if callable(value):
            value = value(request)
        if isinstance(value, LLMResult):
            return value
        if not isinstance(value, Mapping):
            raise LLMProviderError("fake response must be a mapping")
        return LLMResult(data=dict(value), model=request.model, response_id="fake")


class DryRunProvider:
    """Offline provider that records calls and returns an explicit preview.

    It never fabricates a model answer. Supply ``preview`` to exercise a full
    workflow; without it the call fails loudly after being recorded.
    """

    def __init__(
        self,
        preview: Mapping[str, Any] | Callable[[LLMRequest], Mapping[str, Any]] | None = None,
    ) -> None:
        self.preview = preview
        self.requests: list[LLMRequest] = []

    def generate(self, request: LLMRequest) -> LLMResult:
        self.requests.append(request)
        if self.preview is None:
            raise LLMProviderError("dry run recorded; no preview response configured")
        data = self.preview(request) if callable(self.preview) else self.preview
        return LLMResult(data=dict(data), model=request.model, response_id="dry-run")


class ReplayProvider:
    def __init__(self, recordings: Mapping[str, Mapping[str, Any]]) -> None:
        self.recordings = dict(recordings)
        self.requests: list[LLMRequest] = []

    def generate(self, request: LLMRequest) -> LLMResult:
        self.requests.append(request)
        key = request_fingerprint(request)
        if key not in self.recordings:
            raise LLMProviderError(f"no replay recording for request {key}")
        return LLMResult(
            data=dict(self.recordings[key]), model=request.model, response_id=f"replay:{key}"
        )
