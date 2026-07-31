from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Sequence

from ai_math_study.domain.sources import (
    ChapterRange,
    KnowledgeAtom,
    SourceLocator,
    SourceRecord,
    normalize_text,
    stable_hash,
    stable_id,
)


@dataclass(frozen=True)
class PageBlock:
    text: str
    bbox: tuple[float, float, float, float] | None = None


class PDFExtractor(Protocol):
    def page_count(self, path: Path) -> int: ...

    def extract_page(self, path: Path, pdf_page: int) -> Sequence[PageBlock]: ...


class DefaultPDFExtractor:
    """Use PyMuPDF when available; fall back to pypdf without bounding boxes."""

    def page_count(self, path: Path) -> int:
        try:
            import fitz  # type: ignore[import-untyped]

            with fitz.open(path) as document:
                return int(document.page_count)
        except ImportError:
            try:
                from pypdf import PdfReader  # type: ignore[import-not-found]
            except ImportError as exc:
                raise RuntimeError(
                    "PDF ingestion requires PyMuPDF ('fitz') or pypdf; install the pdf extra"
                ) from exc
            return len(PdfReader(str(path)).pages)

    def extract_page(self, path: Path, pdf_page: int) -> Sequence[PageBlock]:
        try:
            import fitz  # type: ignore[import-untyped]

            with fitz.open(path) as document:
                raw_blocks = document[pdf_page - 1].get_text("blocks", sort=True)
            return tuple(
                PageBlock(
                    text=str(block[4]).strip(),
                    bbox=(float(block[0]), float(block[1]), float(block[2]), float(block[3])),
                )
                for block in raw_blocks
                if str(block[4]).strip()
            )
        except ImportError:
            from pypdf import PdfReader  # type: ignore[import-not-found]

            text = PdfReader(str(path)).pages[pdf_page - 1].extract_text() or ""
            return (PageBlock(text=text),) if text.strip() else ()


_SECTION_AT_START = re.compile(r"^\s*(\d+(?:\.\d+)+)\s+([^\n]{1,160})")


def records_from_pdf(
    path: Path,
    *,
    display_path: str,
    chapters: Sequence[ChapterRange],
    source_version: str,
    extractor: PDFExtractor,
) -> tuple[list[SourceRecord], list[KnowledgeAtom]]:
    records: list[SourceRecord] = []
    atoms: list[KnowledgeAtom] = []
    for chapter_range in sorted(chapters, key=lambda item: item.pdf_start):
        current_section: str | None = None
        for pdf_page in range(chapter_range.pdf_start, chapter_range.pdf_end + 1):
            print_page = chapter_range.print_page_for(pdf_page)
            page_anchors = [
                anchor for anchor in chapter_range.sections if anchor.pdf_page == pdf_page
            ]
            if page_anchors:
                current_section = sorted(page_anchors, key=lambda item: item.depth)[0].section
            for block_index, block in enumerate(extractor.extract_page(path, pdf_page)):
                normalized = normalize_text(block.text)
                if not normalized:
                    continue
                section_match = _SECTION_AT_START.match(block.text)
                if section_match and section_match.group(1).startswith(f"{chapter_range.chapter}."):
                    current_section = section_match.group(1)
                    title = section_match.group(2).strip()
                else:
                    matched_anchor = next(
                        (
                            anchor
                            for anchor in sorted(page_anchors, key=lambda item: item.depth, reverse=True)
                            if normalize_text(anchor.title).casefold() in normalized.casefold()
                        ),
                        None,
                    )
                    if matched_anchor is not None:
                        current_section = matched_anchor.section
                    title = f"Chapter {chapter_range.chapter}, page {print_page}, block {block_index + 1}"
                locator = SourceLocator(
                    path=display_path,
                    pdf_page=pdf_page,
                    print_page=print_page,
                    chapter=chapter_range.chapter,
                    section=current_section,
                    bbox=block.bbox,
                )
                digest = stable_hash(normalized)
                source_id = stable_id(
                    "src",
                    "pdf",
                    chapter_range.chapter,
                    pdf_page,
                    block_index,
                    digest,
                )
                records.append(
                    SourceRecord(
                        source_id=source_id,
                        kind="pdf",
                        authority="primary_text",
                        title=title,
                        text=block.text,
                        content_sha256=digest,
                        locator=locator,
                        source_version=source_version,
                        metadata={
                            "block_index": block_index,
                            "formula_text_search_only": True,
                            "requires_visual_formula_verification": True,
                        },
                    )
                )
                atoms.append(
                    KnowledgeAtom(
                        claim_id=stable_id("claim", source_id, digest),
                        source_id=source_id,
                        chapter=chapter_range.chapter,
                        section=current_section,
                        knowledge_type="textbook-block",
                        statement_zh=block.text,
                        english_terms=(),
                        assumptions=(),
                        dependencies=(),
                        conclusion=title,
                        locator=locator,
                        source_version=source_version,
                        content_sha256=digest,
                        # Extracted PDF text is primary evidence, but formulas still
                        # require a visual check against the recorded page and bbox.
                        verification_state="source-aligned",
                    )
                )
    return records, atoms
