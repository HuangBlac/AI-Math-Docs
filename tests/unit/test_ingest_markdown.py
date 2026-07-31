from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_math_study.ingest.markdown import records_from_markdown, split_markdown


class MarkdownIngestTests(unittest.TestCase):
    def test_splits_by_heading_with_line_ranges_and_hierarchy(self) -> None:
        sections = split_markdown(
            "preface\n# Chapter 1\nintro\n## 1.1 Definition\nbody\n",
            "fallback",
        )
        self.assertEqual([item.start_line for item in sections], [1, 2, 4])
        self.assertEqual(sections[-1].end_line, 5)
        self.assertEqual(sections[-1].heading_path, ("Chapter 1", "1.1 Definition"))

    def test_flags_path_title_and_topic_location_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ch2-note.md"
            path.write_text("# Chapter 3 Massart lemma\ncontent", encoding="utf-8")
            records, atoms, reviews = records_from_markdown(
                path,
                display_path="notes/ch2-note.md",
                source_version="test",
                topic_expectations={"Massart": {"chapter": 4, "section": "4.3"}},
            )
        self.assertEqual(len(records), 1)
        self.assertEqual(len(atoms), 1)
        self.assertEqual(atoms[0].locator.start_line, 1)
        self.assertEqual(
            {review.reason for review in reviews},
            {"chapter_signal_conflict", "topic_location_conflict"},
        )


if __name__ == "__main__":
    unittest.main()
