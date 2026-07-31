from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ai_math_study.domain.sources import CorpusManifest, stable_hash
from ai_math_study.ingest import (
    IngestConfig,
    PageBlock,
    build_corpus,
    doctor_corpus,
)
from ai_math_study.retrieval import build_evidence_packet, search_corpus


class FakePDFExtractor:
    def __init__(self, page_count: int = 488) -> None:
        self._page_count = page_count

    def page_count(self, path: Path) -> int:
        return self._page_count

    def extract_page(self, path: Path, pdf_page: int) -> list[PageBlock]:
        return [PageBlock(f"1.1 Risk page {pdf_page}\n风险与 risk", (1.0, 2.0, 3.0, 4.0))]


class IngestPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "中文项目"
        self.root.mkdir()
        self.pdf = self.root / "教材.pdf"
        self.pdf.write_bytes(b"synthetic-pdf")
        self.docs = self.root / "docs" / "computation" / "lftp"
        self.wiki = self.root / "wiki" / "raw" / "lftp"
        self.docs.mkdir(parents=True)
        self.wiki.mkdir(parents=True)
        self.manifest = CorpusManifest.from_dict(
            {
                "pdf_sha256": stable_hash(b"synthetic-pdf"),
                "pdf_page_count": 488,
                "source_version": "fixture-v1",
                "chapters": [
                    {
                        "chapter": 1,
                        "title": "Mathematical Preliminaries",
                        "print_start": 3,
                        "print_end": 4,
                        "pdf_start": 15,
                        "pdf_end": 16,
                    }
                ],
            }
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def config(self) -> IngestConfig:
        return IngestConfig(
            project_root=self.root,
            pdf_path=self.pdf,
            manifest=self.manifest,
            markdown_roots=(self.docs, self.wiki),
            study_dir=self.root / ".study",
            chapters=(1,),
            pdf_extractor=FakePDFExtractor(),
        )

    def test_build_is_idempotent_deduplicates_mirror_and_searches(self) -> None:
        note = "# Chapter 1\n\n## 1.1 Risk\n经验风险 and population risk\n"
        (self.docs / "ch1.md").write_text(note, encoding="utf-8")
        (self.wiki / "ch1.md").write_text(note, encoding="utf-8")

        first = build_corpus(self.config())
        first_manifest = first.manifest_path.read_bytes()
        first_atoms = (first.study_dir / "atoms.jsonl").read_bytes()
        second = build_corpus(self.config())

        self.assertEqual(first_manifest, second.manifest_path.read_bytes())
        self.assertEqual(first_atoms, (second.study_dir / "atoms.jsonl").read_bytes())
        self.assertEqual(first.deduplicated_file_count, 1)
        self.assertTrue(doctor_corpus(first.study_dir).healthy)
        hits = search_corpus(first.database_path, "risk", chapter=1)
        self.assertGreaterEqual(len(hits), 1)
        self.assertTrue(search_corpus(first.database_path, "经验风险", chapter=1))
        pdf_hit = next(
            hit
            for hit in hits
            if hit.authority == "primary_text" and hit.locator["pdf_page"] == 15
        )
        self.assertEqual(pdf_hit.locator["pdf_page"], 15)
        self.assertEqual(pdf_hit.locator["print_page"], 3)
        self.assertEqual(pdf_hit.locator["bbox"], [1.0, 2.0, 3.0, 4.0])
        packet = build_evidence_packet(first.database_path, [pdf_hit])
        self.assertEqual(packet.entries[0].authority, "primary_text")
        self.assertEqual(packet.entries[0].source_version_sha256, self.manifest.pdf_sha256)
        self.assertIn("print p.3", packet.entries[0].locator_label)
        self.assertEqual(packet.corpus_manifest_sha256, first.manifest_sha256)

    def test_divergent_notes_enter_review_queue_without_overwrite(self) -> None:
        (self.docs / "ch1.md").write_text("# Chapter 1\nalpha", encoding="utf-8")
        (self.wiki / "ch1.md").write_text("# Chapter 1\nbeta", encoding="utf-8")
        result = build_corpus(self.config())
        rows = [
            json.loads(line)
            for line in (result.study_dir / "review_queue.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertIn("source_content_conflict", {row["reason"] for row in rows})
        source_rows = (result.study_dir / "sources.jsonl").read_text(encoding="utf-8")
        self.assertIn("alpha", source_rows)
        self.assertIn("beta", source_rows)

    def test_contract_mismatch_fails_before_writing(self) -> None:
        bad = IngestConfig(
            **{**self.config().__dict__, "pdf_extractor": FakePDFExtractor(487)}
        )
        with self.assertRaisesRegex(ValueError, "page count mismatch"):
            build_corpus(bad)
        self.assertFalse((self.root / ".study" / "manifest.json").exists())

    def test_doctor_detects_artifact_tampering(self) -> None:
        (self.docs / "ch1.md").write_text("# Chapter 1\nrisk", encoding="utf-8")
        result = build_corpus(self.config())
        with (result.study_dir / "atoms.jsonl").open("ab") as handle:
            handle.write(b"{}\n")
        report = doctor_corpus(result.study_dir)
        self.assertFalse(report.healthy)
        self.assertTrue(any("hash mismatch" in issue for issue in report.issues))


if __name__ == "__main__":
    unittest.main()
