from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable, Literal, cast

from ai_math_study.domain.evidence import EvidenceEntry, EvidencePacket
from ai_math_study.domain.sources import stable_hash

from .search import SearchHit


def _locator_label(locator: dict[str, object]) -> str:
    labels: list[str] = []
    chapter = locator.get("chapter")
    section = locator.get("section")
    if chapter is not None:
        labels.append(f"Ch {chapter}" + (f" §{section}" if section else ""))
    print_page = locator.get("print_page")
    pdf_page = locator.get("pdf_page")
    if print_page is not None:
        labels.append(f"print p.{print_page}")
    if pdf_page is not None:
        labels.append(f"PDF p.{pdf_page}")
    start_line = locator.get("start_line")
    if start_line is not None:
        end_line = locator.get("end_line") or start_line
        labels.append(f"L{start_line}-{end_line}")
    labels.append(str(locator.get("path", "unknown source")))
    return " | ".join(labels)


def _version_digest(value: str) -> str:
    return value.lower() if re.fullmatch(r"[0-9a-fA-F]{64}", value) else stable_hash(value)


def build_evidence_packet(
    database_path: str | Path,
    hits_or_claim_ids: Iterable[SearchHit | str],
    limit: int = 20,
) -> EvidencePacket:
    """Freeze ranked search hits or explicit claim IDs into a drift-detectable packet."""

    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")
    claim_ids: list[str] = []
    for item in hits_or_claim_ids:
        claim_id = item.claim_id if isinstance(item, SearchHit) else str(item)
        if claim_id not in claim_ids:
            claim_ids.append(claim_id)
        if len(claim_ids) == limit:
            break
    if not claim_ids:
        raise ValueError("at least one claim ID is required")

    placeholders = ",".join("?" for _ in claim_ids)
    connection = sqlite3.connect(str(database_path))
    try:
        meta = connection.execute(
            "SELECT value FROM corpus_meta WHERE key = 'manifest_sha256'"
        ).fetchone()
        if meta is None:
            raise ValueError("corpus database has no manifest digest")
        rows = connection.execute(
            f"""SELECT a.claim_id, a.source_id, a.statement_zh, a.content_sha256,
                       a.locator_json, s.locator_json, s.authority, s.source_version,
                       s.corpus_tier, a.verification_state, a.evidence_type,
                       a.formula_uncertain
                  FROM atoms AS a
                  JOIN sources AS s ON s.source_id = a.source_id
                 WHERE a.claim_id IN ({placeholders})""",
            claim_ids,
        ).fetchall()
    finally:
        connection.close()
    by_id = {row[0]: row for row in rows}
    missing = [claim_id for claim_id in claim_ids if claim_id not in by_id]
    if missing:
        raise ValueError(f"unknown claim IDs: {', '.join(missing)}")

    entries: list[EvidenceEntry] = []
    for index, claim_id in enumerate(claim_ids, 1):
        row = by_id[claim_id]
        atom_locator = json.loads(row[4])
        source_locator = json.loads(row[5])
        locator = atom_locator or source_locator
        authority = row[6]
        if authority not in {"primary_text", "user_note", "derived_wiki", "published_copy"}:
            raise ValueError(f"unsupported evidence authority: {authority}")
        entries.append(
            EvidenceEntry(
                evidence_id=f"E{index:02d}",
                span_id=claim_id,
                source_key=str(locator.get("path", row[1])),
                source_version_sha256=_version_digest(str(row[7])),
                content_sha256=row[3],
                exact_excerpt=row[2],
                authority=authority,
                corpus_tier=cast(Literal["core", "prerequisite"], str(row[8])),
                verification_state=cast(
                    Literal["unverified", "source-aligned", "contradicted", "verified"],
                    str(row[9]),
                ),
                evidence_type=str(row[10]),
                formula_uncertain=bool(row[11]),
                locator_label=_locator_label(locator),
            )
        )
    database = Path(database_path).resolve()
    generation: str | None = database.parent.name
    if generation is not None and not generation.startswith("gen-"):
        generation = None
    return EvidencePacket.freeze(
        str(meta[0]), entries, corpus_generation=generation
    )
