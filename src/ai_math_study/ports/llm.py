"""Provider-neutral structured LLM boundary.

Only final structured answers cross this boundary.  Reasoning traces are neither
requested nor represented by these types.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Protocol, runtime_checkable


@dataclass(frozen=True)
class ProviderProfile:
    provider: str
    model: str
    thinking: bool
    reasoning_effort: Literal["high", "max"] | None = None

    def __post_init__(self) -> None:
        if not self.thinking and self.reasoning_effort is not None:
            raise ValueError("reasoning_effort is only valid when thinking is enabled")


@dataclass(frozen=True)
class LLMCallTelemetry:
    provider: str
    model: str
    thinking: bool
    request_hash: str
    attempt: int
    latency_ms: int
    finish_reason: str | None
    error_code: str | None
    input_tokens: int | None = None
    output_tokens: int | None = None


@runtime_checkable
class TelemetrySink(Protocol):
    def record(self, event: LLMCallTelemetry) -> None: ...


@dataclass(frozen=True)
class LLMRequest:
    model: str
    instructions: str
    input_text: str
    schema_name: str
    json_schema: Mapping[str, Any]
    max_output_tokens: int | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class LLMResult:
    data: Mapping[str, Any]
    model: str
    response_id: str | None = None


@runtime_checkable
class LLMProvider(Protocol):
    def generate(self, request: LLMRequest) -> LLMResult: ...
