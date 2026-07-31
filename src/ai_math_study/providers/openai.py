from __future__ import annotations

import json
import os
from typing import Any

from ai_math_study.ports.llm import LLMRequest, LLMResult
from .errors import (
    LLMProviderError, MissingAPIKeyError, ModelUnavailableError,
    ResponseIncompleteError, ResponseRefusedError,
)


class OpenAIProvider:
    """OpenAI Responses API adapter using strict Structured Outputs."""

    def __init__(self, api_key: str | None = None, client: Any | None = None) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._client = client

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self._api_key:
            raise MissingAPIKeyError("OPENAI_API_KEY is required for OpenAIProvider")
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise LLMProviderError(
                "install the optional 'openai' package to use OpenAIProvider"
            ) from exc
        self._client = OpenAI(api_key=self._api_key)
        return self._client

    def generate(self, request: LLMRequest) -> LLMResult:
        kwargs: dict[str, Any] = {
            "model": request.model,
            "instructions": request.instructions,
            "input": request.input_text,
            "text": {"format": {
                "type": "json_schema", "name": request.schema_name,
                "schema": dict(request.json_schema), "strict": True,
            }},
            "store": False,
        }
        if request.max_output_tokens is not None:
            kwargs["max_output_tokens"] = request.max_output_tokens
        try:
            response = self._get_client().responses.create(**kwargs)
        except LLMProviderError:
            raise
        except Exception as exc:
            name = type(exc).__name__.lower()
            text = str(exc).lower()
            if "notfound" in name or "model" in text and ("not found" in text or "unavailable" in text):
                raise ModelUnavailableError(f"requested model {request.model!r} is unavailable") from exc
            raise LLMProviderError(f"Responses API call failed: {exc}") from exc

        status = getattr(response, "status", "completed")
        if status not in (None, "completed"):
            raise ResponseIncompleteError(f"response status is {status!r}")
        refusal = getattr(response, "refusal", None)
        if refusal:
            raise ResponseRefusedError(str(refusal))
        output_text = getattr(response, "output_text", None)
        if not output_text:
            # SDK response objects may expose refusal only in output content.
            output = getattr(response, "output", ()) or ()
            for item in output:
                for content in getattr(item, "content", ()) or ():
                    if getattr(content, "type", None) == "refusal":
                        raise ResponseRefusedError(str(getattr(content, "refusal", "model refused")))
            raise ResponseIncompleteError("response did not contain structured output text")
        try:
            data = json.loads(output_text)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ResponseIncompleteError("structured output was not valid JSON") from exc
        if not isinstance(data, dict):
            raise ResponseIncompleteError("structured output root must be an object")
        return LLMResult(
            data=data,
            model=getattr(response, "model", request.model),
            response_id=getattr(response, "id", None),
        )
