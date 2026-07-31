from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SearchHit:
    claim_id: str
    source_id: str
    chapter: int | None
    section: str | None
    knowledge_type: str
    statement_zh: str
    conclusion: str
    verification_state: str
    authority: str
    corpus_tier: str
    evidence_type: str
    formula_uncertain: bool
    locator: dict[str, Any]
    rank: float


def _quoted_fts_query(query: str) -> str:
    return '"' + query.replace('"', '""') + '"'


def search_corpus(
    database_path: str | Path,
    query: str,
    limit: int = 20,
    *,
    chapter: int | None = None,
    knowledge_type: str | None = None,
    corpus_tier: str | None = None,
    authority: str | None = None,
    verification_state: str | None = None,
    evidence_type: str | None = None,
    formula_uncertain: bool | None = None,
) -> list[SearchHit]:
    if not query.strip():
        raise ValueError("query must not be empty")
    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")
    use_fts = len(query.strip()) >= 3
    sql = """
        SELECT a.claim_id, a.source_id, a.chapter, a.section, a.knowledge_type,
               a.statement_zh, a.conclusion, a.verification_state,
               s.authority, s.corpus_tier, a.evidence_type, a.formula_uncertain,
               a.locator_json, bm25(atoms_fts) AS rank
          FROM atoms_fts
          JOIN atoms AS a ON a.claim_id = atoms_fts.claim_id
          JOIN sources AS s ON s.source_id = a.source_id
         WHERE atoms_fts MATCH ?
    """
    parameters: list[object] = [query.strip()]
    if not use_fts:
        sql = sql.replace(
            "WHERE atoms_fts MATCH ?",
            "WHERE (instr(a.statement_zh, ?) > 0 OR instr(a.conclusion, ?) > 0 "
            "OR instr(atoms_fts.english_terms, ?) > 0)",
        ).replace("bm25(atoms_fts) AS rank", "0.0 AS rank")
        parameters = [query.strip()] * 3
    if chapter is not None:
        sql += " AND a.chapter = ?"
        parameters.append(chapter)
    if knowledge_type is not None:
        sql += " AND a.knowledge_type = ?"
        parameters.append(knowledge_type)
    for column, value in (
        ("s.corpus_tier", corpus_tier),
        ("s.authority", authority),
        ("a.verification_state", verification_state),
        ("a.evidence_type", evidence_type),
    ):
        if value is not None:
            sql += f" AND {column} = ?"
            parameters.append(value)
    if formula_uncertain is not None:
        sql += " AND a.formula_uncertain = ?"
        parameters.append(int(formula_uncertain))
    sql += " ORDER BY rank, a.claim_id LIMIT ?"
    parameters.append(limit)

    connection = sqlite3.connect(str(database_path))
    try:
        try:
            rows = connection.execute(sql, parameters).fetchall()
        except sqlite3.OperationalError as exc:
            if "fts5" not in str(exc).lower() and "syntax" not in str(exc).lower():
                raise
            parameters[0] = _quoted_fts_query(query.strip())
            rows = connection.execute(sql, parameters).fetchall()
    finally:
        connection.close()
    return [
        SearchHit(
            claim_id=row[0],
            source_id=row[1],
            chapter=row[2],
            section=row[3],
            knowledge_type=row[4],
            statement_zh=row[5],
            conclusion=row[6],
            verification_state=row[7],
            authority=row[8],
            corpus_tier=row[9],
            evidence_type=row[10],
            formula_uncertain=bool(row[11]),
            locator=json.loads(row[12]),
            rank=float(row[13]),
        )
        for row in rows
    ]
