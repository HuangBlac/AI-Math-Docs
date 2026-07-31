from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Mapping, Sequence

from ai_math_study.domain.sources import stable_hash


def build_semantic_manifest(
    *,
    pdf_sha256: str,
    pdf_page_count: int,
    inputs: Sequence[Mapping[str, object]],
    summaries: Mapping[str, object],
    schema_version: int = 2,
    extractor_version: str = "aimath-pdf-v1",
    canonicalizer_version: str = "aimath-text-v1",
    **runtime_sidecar: object,
) -> dict[str, object]:
    """Build the reproducible portion of a corpus manifest.

    Runtime values are deliberately accepted and ignored so callers cannot
    accidentally make a generation ID depend on timestamps or machine paths.
    """

    del runtime_sidecar
    logical_inputs = [dict(row) for row in inputs]
    logical_inputs.sort(key=lambda row: str(row.get("path", "")).casefold())
    return {
        "schema_version": schema_version,
        "pdf": {"sha256": pdf_sha256.lower(), "page_count": pdf_page_count},
        "extractor_version": extractor_version,
        "canonicalizer_version": canonicalizer_version,
        "inputs": logical_inputs,
        "summaries": dict(summaries),
    }


def manifest_digest(manifest: Mapping[str, object]) -> str:
    return stable_hash(dict(manifest))


def generation_id(manifest: Mapping[str, object]) -> str:
    return "gen-" + manifest_digest(manifest)


def publish_generation(study_dir: Path, staging: Path, expected_id: str) -> Path:
    """Publish a complete staging directory then atomically switch CURRENT."""

    if not expected_id.startswith("gen-") or len(expected_id) != 68:
        raise ValueError("invalid generation ID")
    root = study_dir.resolve()
    generations = root / "generations"
    generations.mkdir(parents=True, exist_ok=True)
    destination = generations / expected_id
    if destination.exists():
        shutil.rmtree(staging)
    else:
        os.replace(staging, destination)
    fd, name = tempfile.mkstemp(prefix=".CURRENT.", dir=root)
    try:
        with os.fdopen(fd, "w", encoding="ascii", newline="\n") as handle:
            handle.write(expected_id + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, root / "CURRENT")
    except BaseException:
        Path(name).unlink(missing_ok=True)
        raise
    return destination


def resolve_current_generation(study_dir: Path) -> Path:
    root = study_dir.resolve()
    pointer = (root / "CURRENT").read_text(encoding="ascii").strip()
    if not pointer.startswith("gen-") or Path(pointer).name != pointer:
        raise ValueError("invalid CURRENT pointer")
    generation = root / "generations" / pointer
    if not generation.is_dir():
        raise FileNotFoundError(f"CURRENT generation is missing: {pointer}")
    return generation


def resolve_corpus_database(study_dir: Path) -> Path:
    """Resolve the active DB, while accepting pre-generation study directories."""

    root = study_dir.resolve()
    if (root / "CURRENT").is_file():
        return resolve_current_generation(root) / "corpus.sqlite3"
    return root / "corpus.sqlite3"
