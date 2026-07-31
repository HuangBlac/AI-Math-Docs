from __future__ import annotations

import sqlite3
from pathlib import Path

from ai_math_study.ingest.generation import (
    build_semantic_manifest,
    generation_id,
    publish_generation,
    resolve_corpus_database,
    resolve_current_generation,
)


def test_semantic_manifest_excludes_runtime_noise() -> None:
    left = build_semantic_manifest(
        pdf_sha256="a" * 64,
        pdf_page_count=488,
        inputs=[{"path": "wiki/raw/lftp.pdf", "sha256": "a" * 64, "size": 9}],
        summaries={"claims": [{"id": "c1", "hash": "b" * 64}]},
        created_at="yesterday",
    )
    right = build_semantic_manifest(
        pdf_sha256="a" * 64,
        pdf_page_count=488,
        inputs=[{"size": 9, "sha256": "a" * 64, "path": "wiki/raw/lftp.pdf"}],
        summaries={"claims": [{"hash": "b" * 64, "id": "c1"}]},
        created_at="today",
    )
    assert left == right
    assert generation_id(left) == generation_id(right)


def test_publish_generation_switches_current_without_mutating_old(tmp_path: Path) -> None:
    staging = tmp_path / ".staging-one"
    staging.mkdir()
    (staging / "manifest.json").write_text("{}\n", encoding="utf-8")
    first = publish_generation(tmp_path, staging, "gen-" + "1" * 64)
    assert resolve_current_generation(tmp_path) == first

    staging2 = tmp_path / ".staging-two"
    staging2.mkdir()
    (staging2 / "manifest.json").write_text("{\"v\":2}\n", encoding="utf-8")
    second = publish_generation(tmp_path, staging2, "gen-" + "2" * 64)
    assert resolve_current_generation(tmp_path) == second
    assert (first / "manifest.json").read_text(encoding="utf-8") == "{}\n"
    assert resolve_corpus_database(tmp_path) == second / "corpus.sqlite3"


def test_database_resolution_supports_legacy_root(tmp_path: Path) -> None:
    assert resolve_corpus_database(tmp_path) == tmp_path / "corpus.sqlite3"


def test_schema_has_evidence_facets_and_trigram(tmp_path: Path) -> None:
    migration = Path("src/ai_math_study/migrations/001_initial.sql")
    connection = sqlite3.connect(tmp_path / "corpus.sqlite3")
    connection.executescript(migration.read_text(encoding="utf-8"))
    source_columns = {row[1] for row in connection.execute("pragma table_info(sources)")}
    atom_columns = {row[1] for row in connection.execute("pragma table_info(atoms)")}
    tables = {row[0] for row in connection.execute("select name from sqlite_master")}
    sql = connection.execute(
        "select sql from sqlite_master where name='atoms_fts'"
    ).fetchone()[0]
    assert {"corpus_tier", "authority", "verification_state"} <= source_columns
    assert {"evidence_type", "formula_uncertain"} <= atom_columns
    assert {"contents", "source_facets", "claim_facets"} <= tables
    assert "trigram" in sql
