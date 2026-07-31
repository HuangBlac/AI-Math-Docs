from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

from ai_math_study.state.store import ExerciseOverlay, StateStore


_PDF_SHA256 = "DDEBA8166E4DC2AEDC0B863E67AF9891178A5E13F3316FD672D49CD59E486DEA"
_EXERCISE_COUNTS = {1: 29, 2: 7, 3: 10, 4: 16, 5: 36, 6: 6, 7: 23, 8: 17, 9: 10}
_UNMARKED_COUNTS = {1: 18, 2: 5, 3: 7, 4: 7, 5: 22, 6: 5, 7: 16, 8: 11, 9: 5}
_CLOSED_STATUSES = frozenset({"passed", "corrected", "completed"})


def canonical_exercise_id(value: str) -> str:
    if value.startswith("lftp:"):
        return value
    try:
        chapter_text, number_text = value.removeprefix("Exercise ").split(".", 1)
        chapter, number = int(chapter_text), int(number_text)
    except (ValueError, TypeError) as exc:
        raise ValueError("exercise must look like 1.14") from exc
    if chapter not in _EXERCISE_COUNTS or not 1 <= number <= _EXERCISE_COUNTS[chapter]:
        raise ValueError(f"exercise does not exist in locked LFTP Chapters 1-9: {value}")
    return f"lftp:{_PDF_SHA256}:exercise:{chapter}.{number}"


@dataclass(frozen=True)
class ExerciseInventory:
    chapter: int | None
    total: int
    exercise_ids: tuple[str, ...]
    unmarked: int
    diamond_marked: int
    verification_status: str = "provisional"


@dataclass(frozen=True)
class WeeklySummary:
    total: int
    attempts: int
    closed: int
    remaining: int


class LearningProgressService:
    def __init__(self, store: StateStore, corpus_generation: str) -> None:
        self.store = store
        self.corpus_generation = corpus_generation

    def exercise_inventory(self, chapter: int | None = None) -> ExerciseInventory:
        if chapter is not None and chapter not in _EXERCISE_COUNTS:
            raise ValueError("chapter must be between 1 and 9")
        chapters = (chapter,) if chapter is not None else tuple(_EXERCISE_COUNTS)
        ids = tuple(
            canonical_exercise_id(f"{item}.{number}")
            for item in chapters
            for number in range(1, _EXERCISE_COUNTS[item] + 1)
        )
        unmarked = sum(_UNMARKED_COUNTS[item] for item in chapters)
        return ExerciseInventory(chapter, len(ids), ids, unmarked, len(ids) - unmarked)

    def exercise_status(self, exercise: str) -> ExerciseOverlay:
        return self.store.exercise_overlay(canonical_exercise_id(exercise))

    def record_exercise_attempt(self, exercise: str, answer_path: Path) -> ExerciseOverlay:
        exercise_id = canonical_exercise_id(exercise)
        answer_hash = sha256(answer_path.read_bytes()).hexdigest()
        overlay = self.store.exercise_overlay(exercise_id)
        attempt_id = str(uuid4())
        self.store.record_attempt(
            attempt_id=attempt_id,
            exercise_id=exercise_id,
            expected_version=overlay.version,
            corpus_generation=self.corpus_generation,
            evidence_snapshot={"exercise_id": exercise_id},
            answer_hash=answer_hash,
            outcome="submitted",
            manual_review=False,
            idempotency_key=f"cli-attempt:{attempt_id}",
        )
        return self.store.exercise_overlay(exercise_id)

    def set_exercise_status(self, exercise: str, status: str) -> ExerciseOverlay:
        exercise_id = canonical_exercise_id(exercise)
        overlay = self.store.exercise_overlay(exercise_id)
        self.store.set_exercise_status(
            exercise_id=exercise_id,
            expected_version=overlay.version,
            status=status,
            corpus_generation=self.corpus_generation,
            idempotency_key=f"cli-status:{exercise_id}:{overlay.version + 1}:{status}",
        )
        return self.store.exercise_overlay(exercise_id)

    def weekly_summary(self) -> WeeklySummary:
        inventory = self.exercise_inventory()
        overlays = tuple(self.store.exercise_overlay(item) for item in inventory.exercise_ids)
        attempts = sum(item.attempt_count for item in overlays)
        closed = sum(item.status in _CLOSED_STATUSES for item in overlays)
        return WeeklySummary(inventory.total, attempts, closed, inventory.total - closed)
