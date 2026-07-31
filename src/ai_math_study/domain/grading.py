from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CriterionAssessment:
    criterion_id: str
    level_id: str
    awarded_points: float
    answer_location: str
    reason: str
    correction: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class GradeReport:
    problem_id: str
    score: float
    max_score: float
    assessments: tuple[CriterionAssessment, ...]
    overall_feedback: str
    fatal_misconceptions: tuple[str, ...]
    manual_review: bool
    review_reasons: tuple[str, ...]
    formally_verified: bool = False

    @property
    def percentage(self) -> float:
        return 0.0 if self.max_score == 0 else round(100 * self.score / self.max_score, 2)
