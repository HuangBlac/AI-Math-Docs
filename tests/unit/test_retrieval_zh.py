from __future__ import annotations

from pathlib import Path

from ai_math_study.domain.sources import KnowledgeAtom, SourceLocator, SourceRecord
from ai_math_study.ingest.store import build_sqlite
from ai_math_study.retrieval import search_corpus


def test_chinese_substring_search_uses_trigram_and_short_fallback(tmp_path: Path) -> None:
    locator = SourceLocator(path="lftp.pdf", chapter=4, section="4.2")
    source = SourceRecord(
        source_id="s1", kind="pdf", authority="primary_text", title="ERM",
        text="经验风险最小化", content_sha256="a" * 64, locator=locator,
        source_version="b" * 64,
    )
    atom = KnowledgeAtom(
        claim_id="c1", source_id="s1", chapter=4, section="4.2",
        knowledge_type="definition", statement_zh="经验风险最小化原则",
        english_terms=("empirical risk minimization",), assumptions=(), dependencies=(),
        conclusion="选择经验风险最小的假设", locator=locator,
        source_version="b" * 64, content_sha256="c" * 64,
    )
    db = tmp_path / "corpus.sqlite3"
    build_sqlite(db, [source], [atom], [], manifest_sha256="d" * 64)
    assert search_corpus(db, "风险最小化")[0].claim_id == "c1"
    assert search_corpus(db, "风险")[0].claim_id == "c1"
