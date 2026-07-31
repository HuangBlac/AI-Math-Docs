from __future__ import annotations

import unittest

from ai_math_study.domain.sources import ChapterRange, CorpusManifest, stable_hash


class SourceDomainTests(unittest.TestCase):
    def test_external_manifest_accepts_nested_pdf_and_mapping_chapters(self) -> None:
        manifest = CorpusManifest.from_dict(
            {
                "pdf": {"sha256": "a" * 64, "page_count": 488},
                "chapters": {
                    "1": {
                        "title": "Mathematical Preliminaries",
                        "printed_start": 3,
                        "printed_end": 20,
                        "physical_start": 15,
                        "physical_end": 32,
                    }
                },
            }
        )
        self.assertEqual(manifest.pdf_page_count, 488)
        self.assertEqual(manifest.chapters[0].print_page_for(15), 3)
        self.assertEqual(manifest.chapters[0].print_page_for(32), 20)

    def test_rejects_bad_or_overlapping_page_ranges(self) -> None:
        with self.assertRaisesRegex(ValueError, "different lengths"):
            ChapterRange(1, "Bad", 3, 5, 10, 11)
        with self.assertRaisesRegex(ValueError, "overlap"):
            CorpusManifest(
                "a" * 64,
                488,
                (
                    ChapterRange(1, "One", 3, 4, 10, 11),
                    ChapterRange(2, "Two", 5, 6, 11, 12),
                ),
            )

    def test_hash_is_unicode_stable(self) -> None:
        self.assertEqual(stable_hash("风险"), stable_hash("风险".encode("utf-8")))

    def test_coerces_native_syllabus_and_chapter_spec_shape(self) -> None:
        manifest = CorpusManifest.coerce(
            {
                "source_sha256": "b" * 64,
                "page_count": 488,
                "chapters": [
                    {
                        "chapter": 4,
                        "title_en": "Empirical Risk Minimization",
                        "printed_pages": [71, 107],
                        "pdf_pages": [87, 123],
                        "sections": [
                            {
                                "section": "4.4.4",
                                "title_en": "Beyond Finitely Many Models through Covering Numbers",
                                "printed_page": 89,
                                "pdf_page": 105,
                                "depth": 2,
                            }
                        ],
                    }
                ],
            }
        )
        chapter = manifest.chapters[0]
        self.assertEqual((chapter.pdf_start, chapter.pdf_end), (87, 123))
        self.assertEqual(chapter.sections[0].section, "4.4.4")


if __name__ == "__main__":
    unittest.main()
