from __future__ import annotations

from ai_math_study.ports.llm import LLMRequest, LLMResult
from .errors import LocalOnlyError


class LocalOnlyProvider:
    """Network-incapable provider used to enforce offline workflows."""

    def generate(self, request: LLMRequest) -> LLMResult:
        del request
        raise LocalOnlyError("local-only mode forbids external model generation")
