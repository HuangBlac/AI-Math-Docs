from pathlib import Path

from ai_math_study.state import LearningProgressService, StateStore


GENERATION = "gen-" + "a" * 64


def test_inventory_and_attempt_status_round_trip(tmp_path: Path) -> None:
    service = LearningProgressService(StateStore(tmp_path / "state.sqlite3"), GENERATION)

    inventory = service.exercise_inventory(chapter=9)
    assert inventory.total == 10
    assert inventory.exercise_ids[0].endswith(":exercise:9.1")

    answer = tmp_path / "answer.md"
    answer.write_text("我的证明。", encoding="utf-8")
    overlay = service.record_exercise_attempt("9.1", answer)

    assert overlay.status == "submitted"
    assert overlay.attempt_count == 1
    assert service.exercise_status("9.1").last_attempt_id is not None


def test_weekly_summary_counts_closed_exercises(tmp_path: Path) -> None:
    service = LearningProgressService(StateStore(tmp_path / "state.sqlite3"), GENERATION)
    answer = tmp_path / "answer.md"
    answer.write_text("answer", encoding="utf-8")
    service.record_exercise_attempt("1.1", answer)
    service.set_exercise_status("1.1", "corrected")

    summary = service.weekly_summary()

    assert summary.attempts == 1
    assert summary.closed == 1
    assert summary.total == 154
    assert summary.remaining == 153

