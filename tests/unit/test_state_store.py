from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from ai_math_study.state import (
    IdempotencyMismatch,
    StateConflict,
    StateStore,
)


def test_append_is_idempotent_and_uses_cas(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.sqlite3")
    first = store.append_event(
        aggregate_type="exercise",
        aggregate_id="lftp:sha:exercise:1.1",
        expected_version=0,
        event_type="exercise_started",
        corpus_generation="gen-1",
        evidence_snapshot={"ids": ["claim-1"]},
        payload={"chapter": 1},
        idempotency_key="start-1.1",
    )
    replay = store.append_event(
        aggregate_type="exercise",
        aggregate_id="lftp:sha:exercise:1.1",
        expected_version=0,
        event_type="exercise_started",
        corpus_generation="gen-1",
        evidence_snapshot={"ids": ["claim-1"]},
        payload={"chapter": 1},
        idempotency_key="start-1.1",
    )

    assert first == replay
    assert first.aggregate_version == 1
    assert len(store.events_for("exercise", "lftp:sha:exercise:1.1")) == 1

    with pytest.raises(StateConflict, match="STATE_CONFLICT"):
        store.append_event(
            aggregate_type="exercise",
            aggregate_id="lftp:sha:exercise:1.1",
            expected_version=0,
            event_type="exercise_corrected",
            corpus_generation="gen-1",
            evidence_snapshot={},
            payload={},
            idempotency_key="correct-1.1",
        )


def test_idempotency_key_rejects_different_request(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.sqlite3")
    kwargs = dict(
        aggregate_type="review",
        aggregate_id="review-1",
        expected_version=0,
        event_type="review_resolved",
        corpus_generation="gen-1",
        evidence_snapshot={},
        idempotency_key="resolve-review-1",
    )
    store.append_event(payload={"resolution": "ok"}, **kwargs)
    with pytest.raises(IdempotencyMismatch, match="IDEMPOTENCY_MISMATCH"):
        store.append_event(payload={"resolution": "dismiss"}, **kwargs)


def test_attempt_exercise_and_review_overlays_are_folded(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.sqlite3")
    exercise_id = "lftp:sha:exercise:2.3"
    store.record_attempt(
        attempt_id="attempt-1",
        exercise_id=exercise_id,
        expected_version=0,
        corpus_generation="gen-1",
        evidence_snapshot={"claim": "c1", "hash": "abc"},
        answer_hash="answer-sha",
        outcome="provisional",
        manual_review=True,
        idempotency_key="attempt-1-created",
    )
    assert store.exercise_overlay(exercise_id).status == "in_review"
    assert store.exercise_overlay(exercise_id).attempt_count == 1
    attempt = store.attempt_overlay("attempt-1")
    assert attempt is not None
    assert attempt.exercise_id == exercise_id
    assert attempt.answer_hash == "answer-sha"
    assert attempt.evidence_snapshot_hash

    store.set_exercise_status(
        exercise_id=exercise_id,
        expected_version=1,
        status="corrected",
        corpus_generation="gen-1",
        idempotency_key="exercise-2.3-corrected",
    )
    assert store.exercise_overlay(exercise_id).status == "corrected"

    store.set_review_status(
        review_id="review-9",
        expected_version=0,
        status="resolved",
        corpus_generation="gen-1",
        idempotency_key="review-9-resolved",
    )
    assert store.review_overlay("review-9").status == "resolved"
    assert store.attempt_overlay("missing") is None


def test_doctor_detects_event_gap_and_hash_tampering(tmp_path: Path) -> None:
    path = tmp_path / "state.sqlite3"
    store = StateStore(path)
    event = store.set_review_status(
        review_id="review-1",
        expected_version=0,
        status="resolved",
        corpus_generation="gen-1",
        idempotency_key="review-1-resolved",
    )
    assert store.doctor().ok

    with sqlite3.connect(path) as connection:
        connection.execute(
            "UPDATE events SET payload_json = ? WHERE event_id = ?",
            ('{"status":"tampered"}', event.event_id),
        )
        connection.commit()
    report = store.doctor()
    assert not report.ok
    assert any("hash mismatch" in issue for issue in report.issues)


def test_state_database_survives_unrelated_corpus_rebuild(tmp_path: Path) -> None:
    state_path = tmp_path / ".study" / "state.sqlite3"
    corpus_path = tmp_path / ".study" / "corpus.sqlite3"
    store = StateStore(state_path)
    store.set_review_status(
        review_id="review-1",
        expected_version=0,
        status="resolved",
        corpus_generation="gen-1",
        idempotency_key="review-1-resolved",
    )
    corpus_path.write_bytes(b"first corpus")
    corpus_path.write_bytes(b"rebuilt corpus")

    reopened = StateStore(state_path)
    assert reopened.review_overlay("review-1").status == "resolved"
    assert reopened.pinned_generations() == ("gen-1",)


def test_concurrent_writers_allow_exactly_one_cas_winner(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "state.sqlite3")

    def write(number: int) -> str:
        try:
            store.set_review_status(
                review_id="review-race",
                expected_version=0,
                status="resolved",
                corpus_generation="gen-1",
                idempotency_key=f"race-{number}",
            )
        except StateConflict:
            return "conflict"
        return "written"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(write, (1, 2)))

    assert sorted(results) == ["conflict", "written"]
    assert store.review_overlay("review-race").version == 1
