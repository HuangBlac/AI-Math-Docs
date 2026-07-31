from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from ai_math_study.domain.sources import stable_hash

from .store import file_sha256
from .generation import resolve_current_generation


@dataclass(frozen=True)
class DoctorReport:
    healthy: bool
    issues: tuple[str, ...]
    source_count: int = 0
    atom_count: int = 0
    review_count: int = 0


def doctor_corpus(study_dir: str | Path) -> DoctorReport:
    root = Path(study_dir)
    if (root / "CURRENT").is_file():
        try:
            root = resolve_current_generation(root)
        except (OSError, ValueError) as exc:
            return DoctorReport(False, (f"invalid CURRENT generation: {exc}",))
    issues: list[str] = []
    manifest_path = root / "manifest.json"
    database_path = root / "corpus.sqlite3"
    if not manifest_path.is_file():
        return DoctorReport(False, (f"missing manifest: {manifest_path}",))
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return DoctorReport(False, (f"invalid manifest: {exc}",))

    counts: dict[str, int] = {}
    artifacts = manifest.get("artifacts", {})
    for name in ("sources", "atoms", "review_queue"):
        descriptor = artifacts.get(name)
        if not isinstance(descriptor, dict):
            issues.append(f"missing artifact descriptor: {name}")
            continue
        path = root / str(descriptor.get("file", ""))
        if not path.is_file():
            issues.append(f"missing artifact: {path.name}")
            continue
        actual_hash = file_sha256(path)
        if actual_hash != descriptor.get("sha256"):
            issues.append(f"artifact hash mismatch: {path.name}")
        try:
            actual_count = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        except UnicodeDecodeError:
            issues.append(f"artifact is not valid UTF-8: {path.name}")
            continue
        expected_count = int(descriptor.get("count", -1))
        counts[name] = actual_count
        if actual_count != expected_count:
            issues.append(
                f"artifact count mismatch: {path.name} expected {expected_count}, got {actual_count}"
            )

    if not database_path.is_file():
        issues.append(f"missing database: {database_path.name}")
    else:
        try:
            connection = sqlite3.connect(str(database_path))
            try:
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                if integrity != "ok":
                    issues.append(f"SQLite integrity check failed: {integrity}")
                meta_row = connection.execute(
                    "SELECT value FROM corpus_meta WHERE key = 'manifest_sha256'"
                ).fetchone()
                expected_digest = stable_hash(manifest)
                if meta_row is None or meta_row[0] != expected_digest:
                    issues.append("database was built from a different manifest")
                database_counts = {
                    "sources": connection.execute("SELECT count(*) FROM sources").fetchone()[0],
                    "atoms": connection.execute("SELECT count(*) FROM atoms").fetchone()[0],
                    "review_queue": connection.execute("SELECT count(*) FROM review_queue").fetchone()[0],
                }
                fts_count = connection.execute("SELECT count(*) FROM atoms_fts").fetchone()[0]
                if fts_count != database_counts["atoms"]:
                    issues.append("FTS index count does not match atoms table")
                for name, count in counts.items():
                    if database_counts.get(name) != count:
                        issues.append(f"database count does not match {name}.jsonl")
            finally:
                connection.close()
        except sqlite3.Error as exc:
            issues.append(f"SQLite error: {exc}")

    return DoctorReport(
        healthy=not issues,
        issues=tuple(issues),
        source_count=counts.get("sources", 0),
        atom_count=counts.get("atoms", 0),
        review_count=counts.get("review_queue", 0),
    )
