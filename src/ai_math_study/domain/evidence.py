from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EvidenceIntegrityError(ValueError):
    """A frozen evidence artifact no longer matches its authenticated content."""


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class EvidenceEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(pattern=r"^E\d{2,4}$")
    span_id: str
    source_key: str
    source_version_sha256: str
    content_sha256: str
    exact_excerpt: str
    authority: Literal["primary_text", "user_note", "derived_wiki", "published_copy"]
    corpus_tier: Literal["core", "prerequisite"] = "core"
    verification_state: Literal["unverified", "source-aligned", "contradicted", "verified"] = "unverified"
    evidence_type: str = "extracted_text"
    formula_uncertain: bool = False
    locator_label: str
    entry_sha256: str = ""

    def semantic_data(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude={"entry_sha256"})

    def computed_sha256(self) -> str:
        return sha256(_canonical(self.semantic_data()).encode("utf-8")).hexdigest()

    def seal(self) -> "EvidenceEntry":
        return self.model_copy(update={"entry_sha256": self.computed_sha256()})

    def verify_integrity(self) -> None:
        if not self.entry_sha256 or self.entry_sha256 != self.computed_sha256():
            raise EvidenceIntegrityError(f"entry hash mismatch: {self.evidence_id}")


class EvidencePacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["2.0"] = "2.0"
    packet_id: str
    packet_sha256: str
    corpus_generation: str
    corpus_manifest_sha256: str
    entries: list[EvidenceEntry]

    @model_validator(mode="after")
    def unique_ids(self) -> "EvidencePacket":
        ids = [entry.evidence_id for entry in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("Evidence IDs must be unique")
        for entry in self.entries:
            entry.verify_integrity()
        expected = self.computed_sha256()
        if self.packet_sha256 != expected:
            raise EvidenceIntegrityError("packet hash mismatch")
        if self.packet_id != "packet_" + expected[:20]:
            raise EvidenceIntegrityError("packet id mismatch")
        return self

    def semantic_data(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "corpus_generation": self.corpus_generation,
            "corpus_manifest_sha256": self.corpus_manifest_sha256,
            # List order is evidence ranking and is intentionally authenticated.
            "entries": [entry.model_dump(mode="json") for entry in self.entries],
        }

    def computed_sha256(self) -> str:
        return sha256(_canonical(self.semantic_data()).encode("utf-8")).hexdigest()

    @classmethod
    def freeze(
        cls,
        corpus_manifest_sha256: str,
        entries: list[EvidenceEntry],
        *,
        corpus_generation: str | None = None,
    ) -> "EvidencePacket":
        generation = corpus_generation or "gen-" + sha256(
            corpus_manifest_sha256.encode("utf-8")
        ).hexdigest()
        sealed = [entry.seal() for entry in entries]
        provisional = cls.model_construct(
            schema_version="2.0", packet_id="", packet_sha256="",
            corpus_generation=generation,
            corpus_manifest_sha256=corpus_manifest_sha256, entries=sealed,
        )
        digest = provisional.computed_sha256()
        return cls(
            packet_id="packet_" + digest[:20], packet_sha256=digest,
            corpus_generation=generation,
            corpus_manifest_sha256=corpus_manifest_sha256, entries=sealed,
        )

    def allowed_ids(self) -> set[str]:
        return {entry.evidence_id for entry in self.entries}
