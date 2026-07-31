"""Domain contracts for evidence-preserving note organization.

The note workflow deliberately keeps model decisions separate from deterministic
assembly, validation, and file mutation.  These dataclasses contain final structured
answers only; no hidden reasoning is represented or persisted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class NoteIssue:
    severity: str
    code: str
    message: str
    line: int | None = None
    token: str | None = None
    section_id: str | None = None

    @property
    def is_error(self) -> bool:
        return self.severity == "error"


@dataclass(frozen=True)
class NoteFragment:
    fragment_id: str
    markdown: str
    heading_hint: str | None = None

    def as_prompt_data(self) -> dict[str, Any]:
        return {
            "fragment_id": self.fragment_id,
            "heading_hint": self.heading_hint,
            "markdown": self.markdown,
        }


@dataclass(frozen=True)
class NotePlanSection:
    section_id: str
    heading: str
    source_fragment_ids: tuple[str, ...]
    instructions: str

    def as_prompt_data(self) -> dict[str, Any]:
        return {
            "section_id": self.section_id,
            "heading": self.heading,
            "source_fragment_ids": list(self.source_fragment_ids),
            "instructions": self.instructions,
        }


@dataclass(frozen=True)
class NotePlan:
    document_title: str
    sections: tuple[NotePlanSection, ...]


@dataclass(frozen=True)
class SectionRewrite:
    section_id: str
    body_markdown: str


@dataclass(frozen=True)
class NoteCritique:
    approved: bool
    summary: str
    issues: tuple[NoteIssue, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class MathRepairSuggestion:
    token: str
    original_math: str
    replacement_math: str
    rationale: str
    confidence: float
    requires_manual_review: bool = True


@dataclass(frozen=True)
class NoteProposal:
    source_name: str
    source_sha256: str
    original_markdown: str
    proposed_markdown: str
    unified_diff: str
    plan: NotePlan
    critique: NoteCritique
    validation_issues: tuple[NoteIssue, ...]
    provider_metadata: Mapping[str, Any] = field(default_factory=dict)
    source_had_utf8_bom: bool = False
    applied: bool = False

    @property
    def eligible_to_apply(self) -> bool:
        return (
            self.critique.approved
            and not any(issue.is_error for issue in self.critique.issues)
            and not any(issue.is_error for issue in self.validation_issues)
        )

