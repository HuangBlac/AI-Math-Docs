PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS corpus_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    authority TEXT NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    locator_json TEXT NOT NULL,
    source_version TEXT NOT NULL,
    mirror_paths_json TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    corpus_tier TEXT NOT NULL DEFAULT 'core',
    verification_state TEXT NOT NULL DEFAULT 'unverified'
);

CREATE TABLE IF NOT EXISTS contents (
    content_sha256 TEXT PRIMARY KEY,
    canonical_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_facets (
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    facet_key TEXT NOT NULL,
    facet_value TEXT NOT NULL,
    PRIMARY KEY (source_id, facet_key, facet_value)
);

CREATE TABLE IF NOT EXISTS atoms (
    claim_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    chapter INTEGER,
    section TEXT,
    knowledge_type TEXT NOT NULL,
    statement_zh TEXT NOT NULL,
    english_terms_json TEXT NOT NULL,
    assumptions_json TEXT NOT NULL,
    dependencies_json TEXT NOT NULL,
    conclusion TEXT NOT NULL,
    locator_json TEXT NOT NULL,
    source_version TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    verification_state TEXT NOT NULL,
    misconception_tags_json TEXT NOT NULL,
    evidence_type TEXT NOT NULL DEFAULT 'extracted_text',
    formula_uncertain INTEGER NOT NULL DEFAULT 0 CHECK(formula_uncertain IN (0, 1))
);

CREATE TABLE IF NOT EXISTS claim_facets (
    claim_id TEXT NOT NULL REFERENCES atoms(claim_id),
    facet_key TEXT NOT NULL,
    facet_value TEXT NOT NULL,
    PRIMARY KEY (claim_id, facet_key, facet_value)
);

CREATE TABLE IF NOT EXISTS review_queue (
    review_id TEXT PRIMARY KEY,
    reason TEXT NOT NULL,
    source_ids_json TEXT NOT NULL,
    details_json TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS atoms_fts USING fts5(
    claim_id UNINDEXED,
    statement_zh,
    conclusion,
    english_terms,
    tokenize = 'trigram'
);
