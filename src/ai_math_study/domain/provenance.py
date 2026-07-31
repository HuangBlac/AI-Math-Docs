from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RunProvenance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    created_at: str
    requested_model: str
    actual_model: str | None = None
    response_id: str | None = None
    prompt_sha256: str
    schema_version: str
    config_sha256: str
    corpus_manifest_sha256: str | None = None
    evidence_packet_id: str | None = None
    parent_run_id: str | None = None
    provider: str
    store: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        requested_model: str,
        prompt: str,
        schema_version: str,
        config: dict[str, Any],
        provider: str,
        **kwargs: Any,
    ) -> "RunProvenance":
        now = datetime.now(timezone.utc).isoformat()
        config_json = json.dumps(config, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        seed = f"{now}\x1f{requested_model}\x1f{prompt}\x1f{config_json}\x1f{provider}"
        return cls(
            run_id="run_" + sha256(seed.encode("utf-8")).hexdigest()[:20],
            created_at=now,
            requested_model=requested_model,
            prompt_sha256=sha256(prompt.encode("utf-8")).hexdigest(),
            schema_version=schema_version,
            config_sha256=sha256(config_json.encode("utf-8")).hexdigest(),
            provider=provider,
            store=False,
            **kwargs,
        )

