from __future__ import annotations

import os
import sqlite3
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from ai_math_study.domain.sources import (
    KnowledgeAtom,
    ReviewItem,
    SourceRecord,
    canonical_json,
    stable_hash,
)


def file_sha256(path: Path) -> str:
    from hashlib import sha256

    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jsonl_bytes(rows: Iterable[dict]) -> bytes:
    return b"".join((canonical_json(row) + "\n").encode("utf-8") for row in rows)


def write_if_changed(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return
    handle, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as output:
            output.write(payload)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    write_if_changed(path, jsonl_bytes(rows))


def build_sqlite(
    path: Path,
    sources: Iterable[SourceRecord],
    atoms: Iterable[KnowledgeAtom],
    reviews: Iterable[ReviewItem],
    *,
    manifest_sha256: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    migration = Path(__file__).resolve().parents[1] / "migrations" / "001_initial.sql"
    try:
        connection = sqlite3.connect(str(temporary))
        try:
            connection.executescript(migration.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT INTO corpus_meta(key, value) VALUES (?, ?)",
                ("manifest_sha256", manifest_sha256),
            )
            for source in sorted(sources, key=lambda item: item.source_id):
                connection.execute(
                    """INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        source.source_id,
                        source.kind,
                        source.authority,
                        source.title,
                        source.text,
                        source.content_sha256,
                        canonical_json(asdict(source.locator)),
                        source.source_version,
                        canonical_json(source.mirror_paths),
                        canonical_json(dict(source.metadata)),
                        source.corpus_tier,
                        source.verification_state,
                    ),
                )
                connection.execute(
                    "INSERT OR IGNORE INTO contents VALUES (?, ?)",
                    (source.content_sha256, source.text),
                )
                connection.executemany(
                    "INSERT OR IGNORE INTO source_facets VALUES (?, ?, ?)",
                    (
                        (source.source_id, "corpus_tier", source.corpus_tier),
                        (source.source_id, "authority", source.authority),
                        (source.source_id, "verification_state", source.verification_state),
                    ),
                )
                for key, value in sorted(dict(source.metadata).items()):
                    if key in {"corpus_tier", "verification_state"}:
                        connection.execute(
                            "INSERT OR IGNORE INTO source_facets VALUES (?, ?, ?)",
                            (source.source_id, key, str(value)),
                        )
                for mirror in source.mirror_paths:
                    connection.execute(
                        "INSERT OR IGNORE INTO source_facets VALUES (?, ?, ?)",
                        (source.source_id, "mirror_path", mirror),
                    )
            for atom in sorted(atoms, key=lambda item: item.claim_id):
                connection.execute(
                    """INSERT INTO atoms VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )""",
                    (
                        atom.claim_id,
                        atom.source_id,
                        atom.chapter,
                        atom.section,
                        atom.knowledge_type,
                        atom.statement_zh,
                        canonical_json(atom.english_terms),
                        canonical_json(atom.assumptions),
                        canonical_json(atom.dependencies),
                        atom.conclusion,
                        canonical_json(asdict(atom.locator)),
                        atom.source_version,
                        atom.content_sha256,
                        atom.verification_state,
                        canonical_json(atom.misconception_tags),
                        atom.evidence_type,
                        int(atom.formula_uncertain),
                    ),
                )
                connection.execute(
                    "INSERT OR IGNORE INTO claim_facets VALUES (?, ?, ?)",
                    (atom.claim_id, "verification_state", atom.verification_state),
                )
                connection.execute(
                    "INSERT OR IGNORE INTO claim_facets VALUES (?, ?, ?)",
                    (atom.claim_id, "evidence_type", atom.evidence_type),
                )
                connection.execute(
                    "INSERT OR IGNORE INTO claim_facets VALUES (?, ?, ?)",
                    (atom.claim_id, "formula_uncertain", str(int(atom.formula_uncertain))),
                )
                connection.execute(
                    "INSERT INTO atoms_fts VALUES (?, ?, ?, ?)",
                    (
                        atom.claim_id,
                        atom.statement_zh,
                        atom.conclusion,
                        " ".join(atom.english_terms),
                    ),
                )
            for review in sorted(reviews, key=lambda item: item.review_id):
                connection.execute(
                    "INSERT INTO review_queue VALUES (?, ?, ?, ?, ?)",
                    (
                        review.review_id,
                        review.reason,
                        canonical_json(review.source_ids),
                        canonical_json(dict(review.details)),
                        review.status,
                    ),
                )
            connection.commit()
        finally:
            connection.close()
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def artifact_descriptor(path: Path, count: int) -> dict[str, object]:
    return {"file": path.name, "count": count, "sha256": file_sha256(path)}


def stable_manifest_digest(manifest: dict[str, object]) -> str:
    return stable_hash(manifest)
