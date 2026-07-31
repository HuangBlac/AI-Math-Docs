from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

from .evidence import EvidenceEntry, EvidencePacket


def content_digest(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


class ProblemType(str, Enum):
    PROOF = "proof"
    COUNTEREXAMPLE = "counterexample"
    GAP_FILL = "gap_fill"


def allowed_evidence_ids(packet: EvidencePacket) -> frozenset[str]:
    return frozenset(packet.allowed_ids())


def evidence_as_prompt_data(packet: EvidencePacket) -> list[dict[str, str]]:
    return [
        {
            "evidence_id": entry.evidence_id,
            "source_locator": entry.locator_label,
            "authority": entry.authority,
            "text": entry.exact_excerpt,
        }
        for entry in packet.entries
    ]


def drifted_evidence_ids(
    packet: EvidencePacket, current_text: Mapping[str, str] | None,
) -> tuple[str, ...]:
    if current_text is None:
        return ()
    return tuple(
        entry.evidence_id
        for entry in packet.entries
        if entry.evidence_id not in current_text
        or content_digest(current_text[entry.evidence_id]) != entry.content_sha256
    )


def has_primary_evidence(packet: EvidencePacket) -> bool:
    return any(entry.authority in {"primary_text", "published_copy"} for entry in packet.entries)


@dataclass(frozen=True)
class RubricLevel:
    level_id: str
    description: str
    multiplier: float

    def __post_init__(self) -> None:
        if not 0 <= self.multiplier <= 1:
            raise ValueError("rubric multiplier must be between 0 and 1")


@dataclass(frozen=True)
class RubricCriterion:
    criterion_id: str
    description: str
    max_points: float
    levels: tuple[RubricLevel, ...]

    def __post_init__(self) -> None:
        if self.max_points <= 0 or not self.levels:
            raise ValueError("criterion requires positive points and at least one level")
        if len({level.level_id for level in self.levels}) != len(self.levels):
            raise ValueError("rubric level ids must be unique within a criterion")


@dataclass(frozen=True)
class GeneratedProblem:
    problem_id: str
    problem_type: ProblemType
    statement: str
    solution_outline: str
    evidence_ids: tuple[str, ...]
    rubric: tuple[RubricCriterion, ...]
    evidence_packet_id: str
    evidence_packet_hash: str
    manual_review: bool = False
    review_reasons: tuple[str, ...] = field(default_factory=tuple)


def packet_digest(packet: EvidencePacket) -> str:
    return packet.computed_sha256()


@dataclass(frozen=True)
class EvidenceDecision:
    may_apply_deduction: bool
    may_advance_mastery: bool
    may_release_answer: bool
    manual_review: bool
    reasons: tuple[str, ...]


def evidence_decision(
    packet: EvidencePacket,
    *,
    deduction_evidence_ids: tuple[str, ...] = (),
    manual_review: bool = False,
) -> EvidenceDecision:
    """Fail-closed policy shared by grading, mastery, and answer release."""

    reasons: list[str] = []
    provisional = [
        entry.evidence_id for entry in packet.entries
        if entry.verification_state not in {"source-aligned", "verified"}
    ]
    if provisional:
        reasons.append("provisional evidence: " + ", ".join(provisional))
    if manual_review:
        reasons.append("manual_review required")
    selected = [entry for entry in packet.entries if entry.evidence_id in deduction_evidence_ids]
    if deduction_evidence_ids and (
        not selected or all(entry.formula_uncertain for entry in selected)
    ):
        reasons.append("formula_uncertain evidence cannot be the sole basis for deduction")
    blocked = bool(reasons)
    return EvidenceDecision(
        may_apply_deduction=not blocked,
        may_advance_mastery=not blocked,
        may_release_answer=not blocked,
        manual_review=blocked,
        reasons=tuple(reasons),
    )


__all__ = [
    "EvidenceEntry", "EvidencePacket", "GeneratedProblem", "ProblemType",
    "RubricCriterion", "RubricLevel", "allowed_evidence_ids",
    "drifted_evidence_ids", "evidence_as_prompt_data", "has_primary_evidence",
    "packet_digest", "EvidenceDecision", "evidence_decision",
]
