from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from typing import Any


def stable_id(prefix: str, *parts: object, length: int = 16) -> str:
    payload = "\x1f".join(str(part) for part in parts)
    return f"{prefix}_{sha256(payload.encode('utf-8')).hexdigest()[:length]}"


@dataclass(frozen=True)
class SourceLocator:
    path: str
    start_line: int | None = None
    end_line: int | None = None
    pdf_page_start: int | None = None
    pdf_page_end: int | None = None
    book_page_start: int | None = None
    book_page_end: int | None = None
    chapter: int | None = None
    section: str | None = None

    def label(self) -> str:
        labels = [self.path]
        if self.start_line is not None:
            end = self.end_line if self.end_line is not None else self.start_line
            labels.append(f"L{self.start_line}-L{end}")
        if self.book_page_start is not None:
            end = self.book_page_end or self.book_page_start
            labels.append(f"book p.{self.book_page_start}-{end}")
        if self.pdf_page_start is not None:
            end = self.pdf_page_end or self.pdf_page_start
            labels.append(f"PDF p.{self.pdf_page_start}-{end}")
        if self.section:
            labels.append(f"sec. {self.section}")
        return " | ".join(labels)


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    title: str
    heading_path: list[str]
    text: str
    locator: SourceLocator
    content_sha256: str
    kind: str = "markdown"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceRecord":
        copy = dict(data)
        copy["locator"] = SourceLocator(**copy["locator"])
        return cls(**copy)


@dataclass(frozen=True)
class RubricCriterion:
    criterion_id: str
    description: str
    points: int
    source_ids: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RubricCriterion":
        return cls(**data)


@dataclass
class Question:
    question_id: str
    question_type: str
    chapter: int
    section: str
    difficulty: str
    prompt: str
    expected_form: str
    source_ids: list[str]
    rubric: list[RubricCriterion]
    reference_answer: str
    common_misconceptions: list[str]
    verification_checks: list[str]
    generation_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Question":
        copy = dict(data)
        copy["rubric"] = [RubricCriterion.from_dict(item) for item in copy["rubric"]]
        return cls(**copy)


@dataclass(frozen=True)
class CriterionScore:
    criterion_id: str
    awarded: int
    possible: int
    reason: str
    source_ids: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CriterionScore":
        return cls(**data)


@dataclass(frozen=True)
class Misconception:
    claim: str
    diagnosis: str
    correction: str
    severity: str
    source_ids: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Misconception":
        return cls(**data)


@dataclass
class GradeReport:
    question_id: str
    criterion_scores: list[CriterionScore]
    misconceptions: list[Misconception]
    strengths: list[str]
    next_steps: list[str]
    model_score: int
    verified_score: int
    verdict: str
    needs_human_review: bool
    verification_issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

