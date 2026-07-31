from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping
from uuid import UUID, uuid4

from ai_math_study.domain.sources import canonical_json, stable_hash


class StateError(RuntimeError):
    code = "STATE_ERROR"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")


class StateConflict(StateError):
    code = "STATE_CONFLICT"


class IdempotencyMismatch(StateError):
    code = "IDEMPOTENCY_MISMATCH"


@dataclass(frozen=True)
class StateEvent:
    event_id: str
    idempotency_key: str
    aggregate_type: str
    aggregate_id: str
    aggregate_version: int
    event_type: str
    corpus_generation: str
    evidence_snapshot: Mapping[str, Any]
    evidence_snapshot_hash: str
    payload: Mapping[str, Any]
    created_at: str


@dataclass(frozen=True)
class AttemptOverlay:
    attempt_id: str
    exercise_id: str
    answer_hash: str
    outcome: str
    manual_review: bool
    corpus_generation: str
    evidence_snapshot_hash: str


@dataclass(frozen=True)
class ExerciseOverlay:
    exercise_id: str
    version: int
    status: str
    attempt_count: int
    last_attempt_id: str | None


@dataclass(frozen=True)
class ReviewOverlay:
    review_id: str
    version: int
    status: str


@dataclass(frozen=True)
class DoctorReport:
    ok: bool
    event_count: int
    pinned_generation_count: int
    issues: tuple[str, ...]


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _event_from_row(row: sqlite3.Row) -> StateEvent:
    return StateEvent(
        event_id=row["event_id"],
        idempotency_key=row["idempotency_key"],
        aggregate_type=row["aggregate_type"],
        aggregate_id=row["aggregate_id"],
        aggregate_version=row["aggregate_version"],
        event_type=row["event_type"],
        corpus_generation=row["corpus_generation"],
        evidence_snapshot=json.loads(row["evidence_snapshot_json"]),
        evidence_snapshot_hash=row["evidence_snapshot_hash"],
        payload=json.loads(row["payload_json"]),
        created_at=row["created_at"],
    )


class StateStore:
    """Append-only learning-state ledger, intentionally separate from corpus storage."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._migrate()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=30000")
        return connection

    def _migrate(self) -> None:
        migration = Path(__file__).parent / "migrations" / "001_state.sql"
        sql = migration.read_text(encoding="utf-8")
        checksum = sha256(sql.encode("utf-8")).hexdigest()
        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_migrations'"
            ).fetchone()
            if not exists:
                connection.executescript(sql)
                connection.execute(
                    "INSERT INTO schema_migrations VALUES (?, ?, ?)", (1, checksum, _now())
                )
            else:
                row = connection.execute(
                    "SELECT checksum FROM schema_migrations WHERE version=1"
                ).fetchone()
                if row is None or row["checksum"] != checksum:
                    raise StateError("state migration checksum mismatch")

    def append_event(
        self,
        *,
        aggregate_type: str,
        aggregate_id: str,
        expected_version: int,
        event_type: str,
        corpus_generation: str,
        evidence_snapshot: Mapping[str, Any],
        payload: Mapping[str, Any],
        idempotency_key: str,
    ) -> StateEvent:
        if expected_version < 0:
            raise ValueError("expected_version must be non-negative")
        evidence_json = canonical_json(dict(evidence_snapshot))
        payload_json = canonical_json(dict(payload))
        request_hash = stable_hash(
            {
                "aggregate_type": aggregate_type,
                "aggregate_id": aggregate_id,
                "expected_version": expected_version,
                "event_type": event_type,
                "corpus_generation": corpus_generation,
                "evidence_snapshot": evidence_snapshot,
                "payload": payload,
            }
        )
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            prior = connection.execute(
                "SELECT * FROM events WHERE idempotency_key=?", (idempotency_key,)
            ).fetchone()
            if prior is not None:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyMismatch(idempotency_key)
                connection.rollback()
                return _event_from_row(prior)
            row = connection.execute(
                "SELECT COALESCE(MAX(aggregate_version), 0) AS version FROM events "
                "WHERE aggregate_type=? AND aggregate_id=?",
                (aggregate_type, aggregate_id),
            ).fetchone()
            current_version = int(row["version"])
            if current_version != expected_version:
                raise StateConflict(
                    f"{aggregate_type}/{aggregate_id}: expected {expected_version}, "
                    f"current {current_version}"
                )
            event_id = str(uuid4())
            created_at = _now()
            connection.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id,
                    idempotency_key,
                    request_hash,
                    aggregate_type,
                    aggregate_id,
                    current_version + 1,
                    event_type,
                    corpus_generation,
                    evidence_json,
                    stable_hash(evidence_snapshot),
                    payload_json,
                    stable_hash(payload),
                    created_at,
                ),
            )
            connection.commit()
            return StateEvent(
                event_id=event_id,
                idempotency_key=idempotency_key,
                aggregate_type=aggregate_type,
                aggregate_id=aggregate_id,
                aggregate_version=current_version + 1,
                event_type=event_type,
                corpus_generation=corpus_generation,
                evidence_snapshot=dict(evidence_snapshot),
                evidence_snapshot_hash=stable_hash(evidence_snapshot),
                payload=dict(payload),
                created_at=created_at,
            )
        except sqlite3.IntegrityError as exc:
            connection.rollback()
            raise StateConflict(str(exc)) from exc
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def events_for(self, aggregate_type: str, aggregate_id: str) -> tuple[StateEvent, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM events WHERE aggregate_type=? AND aggregate_id=? "
                "ORDER BY aggregate_version",
                (aggregate_type, aggregate_id),
            ).fetchall()
        return tuple(_event_from_row(row) for row in rows)

    def record_attempt(
        self,
        *,
        attempt_id: str,
        exercise_id: str,
        expected_version: int,
        corpus_generation: str,
        evidence_snapshot: Mapping[str, Any],
        answer_hash: str,
        outcome: str,
        manual_review: bool,
        idempotency_key: str,
    ) -> StateEvent:
        return self.append_event(
            aggregate_type="exercise",
            aggregate_id=exercise_id,
            expected_version=expected_version,
            event_type="attempt_recorded",
            corpus_generation=corpus_generation,
            evidence_snapshot=evidence_snapshot,
            payload={
                "attempt_id": attempt_id,
                "answer_hash": answer_hash,
                "outcome": outcome,
                "manual_review": manual_review,
            },
            idempotency_key=idempotency_key,
        )

    def set_exercise_status(
        self,
        *,
        exercise_id: str,
        expected_version: int,
        status: str,
        corpus_generation: str,
        idempotency_key: str,
    ) -> StateEvent:
        return self.append_event(
            aggregate_type="exercise",
            aggregate_id=exercise_id,
            expected_version=expected_version,
            event_type="exercise_status_set",
            corpus_generation=corpus_generation,
            evidence_snapshot={},
            payload={"status": status},
            idempotency_key=idempotency_key,
        )

    def set_review_status(
        self,
        *,
        review_id: str,
        expected_version: int,
        status: str,
        corpus_generation: str,
        idempotency_key: str,
    ) -> StateEvent:
        event_type = {
            "resolved": "review_resolved",
            "dismissed": "review_dismissed",
            "open": "review_reopened",
        }.get(status, "review_status_set")
        return self.append_event(
            aggregate_type="review",
            aggregate_id=review_id,
            expected_version=expected_version,
            event_type=event_type,
            corpus_generation=corpus_generation,
            evidence_snapshot={},
            payload={"status": status},
            idempotency_key=idempotency_key,
        )

    def exercise_overlay(self, exercise_id: str) -> ExerciseOverlay:
        events = self.events_for("exercise", exercise_id)
        status = "not_started"
        attempt_count = 0
        last_attempt_id: str | None = None
        for event in events:
            if event.event_type == "attempt_recorded":
                attempt_count += 1
                last_attempt_id = str(event.payload["attempt_id"])
                status = "in_review" if event.payload.get("manual_review") else str(
                    event.payload.get("outcome", "submitted")
                )
            elif "status" in event.payload:
                status = str(event.payload["status"])
        return ExerciseOverlay(exercise_id, len(events), status, attempt_count, last_attempt_id)

    def attempt_overlay(self, attempt_id: str) -> AttemptOverlay | None:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM events WHERE event_type='attempt_recorded' "
                "ORDER BY created_at, event_id"
            ).fetchall()
        for row in rows:
            event = _event_from_row(row)
            if event.payload.get("attempt_id") == attempt_id:
                return AttemptOverlay(
                    attempt_id=attempt_id,
                    exercise_id=event.aggregate_id,
                    answer_hash=str(event.payload["answer_hash"]),
                    outcome=str(event.payload["outcome"]),
                    manual_review=bool(event.payload["manual_review"]),
                    corpus_generation=event.corpus_generation,
                    evidence_snapshot_hash=event.evidence_snapshot_hash,
                )
        return None

    def review_overlay(self, review_id: str) -> ReviewOverlay:
        events = self.events_for("review", review_id)
        status = "open"
        for event in events:
            status = str(event.payload.get("status", status))
        return ReviewOverlay(review_id, len(events), status)

    def pinned_generations(self) -> tuple[str, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT DISTINCT corpus_generation FROM events ORDER BY corpus_generation"
            ).fetchall()
        return tuple(row[0] for row in rows)

    def doctor(self) -> DoctorReport:
        issues: list[str] = []
        with self._connect() as connection:
            quick = connection.execute("PRAGMA quick_check").fetchone()[0]
            if quick != "ok":
                issues.append(f"sqlite quick_check: {quick}")
            rows = connection.execute(
                "SELECT * FROM events ORDER BY aggregate_type, aggregate_id, aggregate_version"
            ).fetchall()
            expected: dict[tuple[str, str], int] = {}
            for row in rows:
                key = (row["aggregate_type"], row["aggregate_id"])
                wanted = expected.get(key, 1)
                if row["aggregate_version"] != wanted:
                    issues.append(f"aggregate version gap for {key}: expected {wanted}")
                expected[key] = row["aggregate_version"] + 1
                try:
                    UUID(row["event_id"])
                except ValueError:
                    issues.append(f"invalid event UUID: {row['event_id']}")
                for field in ("evidence_snapshot", "payload"):
                    raw = row[f"{field}_json"]
                    try:
                        value = json.loads(raw)
                    except json.JSONDecodeError:
                        issues.append(f"{field} invalid JSON for {row['event_id']}")
                        continue
                    if stable_hash(value) != row[f"{field}_hash"]:
                        issues.append(f"{field} hash mismatch for {row['event_id']}")
            generations = connection.execute(
                "SELECT COUNT(DISTINCT corpus_generation) FROM events"
            ).fetchone()[0]
        return DoctorReport(not issues, len(rows), generations, tuple(issues))
