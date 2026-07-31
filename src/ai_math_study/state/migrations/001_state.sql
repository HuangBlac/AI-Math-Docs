CREATE TABLE schema_migrations (
    version INTEGER PRIMARY KEY,
    checksum TEXT NOT NULL,
    applied_at TEXT NOT NULL
);

CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    request_hash TEXT NOT NULL,
    aggregate_type TEXT NOT NULL CHECK (aggregate_type IN (
        'attempt', 'exercise', 'review', 'diagnostic', 'formula', 'mastery',
        'answer_release', 'weekly_hours', 'progress'
    )),
    aggregate_id TEXT NOT NULL,
    aggregate_version INTEGER NOT NULL CHECK (aggregate_version > 0),
    event_type TEXT NOT NULL CHECK (event_type IN (
        'attempt_recorded', 'exercise_started', 'exercise_submitted',
        'exercise_corrected', 'exercise_status_set', 'review_resolved',
        'review_dismissed', 'review_reopened', 'review_status_set',
        'diagnostic_recorded', 'formula_verified', 'mastery_recorded',
        'answer_released', 'weekly_hours_recorded', 'progress_recorded'
    )),
    corpus_generation TEXT NOT NULL,
    evidence_snapshot_json TEXT NOT NULL,
    evidence_snapshot_hash TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (aggregate_type, aggregate_id, aggregate_version)
);

CREATE INDEX events_aggregate_idx
ON events(aggregate_type, aggregate_id, aggregate_version);

CREATE INDEX events_generation_idx ON events(corpus_generation);
