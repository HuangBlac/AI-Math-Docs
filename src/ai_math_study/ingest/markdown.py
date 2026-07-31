from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, cast

from ai_math_study.domain.sources import (
    KnowledgeAtom,
    ReviewItem,
    SourceLocator,
    SourceRecord,
    normalize_text,
    stable_hash,
    stable_id,
)


_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_CHAPTER_IN_PATH = re.compile(r"(?:^|[-_/\\])ch(?:apter)?[-_ ]?(\d+)(?:\D|$)", re.I)
_CHAPTER_IN_TITLE = re.compile(r"(?:chapter|第)\s*(\d+)\s*(?:章)?", re.I)
_SECTION = re.compile(r"(?<!\d)(\d+(?:\.\d+)+)(?!\d)")


@dataclass(frozen=True)
class MarkdownSection:
    title: str
    heading_path: tuple[str, ...]
    text: str
    start_line: int
    end_line: int


def split_markdown(text: str, fallback_title: str) -> list[MarkdownSection]:
    """Split Markdown at headings while retaining exact one-based line ranges."""

    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines, 1):
        match = _HEADING.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))

    sections: list[MarkdownSection] = []
    stack: list[tuple[int, str]] = []
    starts = headings or [(1, 1, fallback_title)]
    if headings and headings[0][0] > 1 and any(line.strip() for line in lines[: headings[0][0] - 1]):
        starts = [(1, 0, fallback_title), *headings]

    for position, (start, level, title) in enumerate(starts):
        end = (starts[position + 1][0] - 1) if position + 1 < len(starts) else len(lines)
        if level:
            stack = [item for item in stack if item[0] < level]
            stack.append((level, title))
        body = "\n".join(lines[start - 1 : end]).strip()
        if not body:
            continue
        sections.append(
            MarkdownSection(
                title=title,
                heading_path=tuple(item[1] for item in stack) if stack else (title,),
                text=body,
                start_line=start,
                end_line=end,
            )
        )
    return sections


def infer_chapter(path: Path, title: str) -> tuple[int | None, tuple[int, ...]]:
    signals: list[int] = []
    path_match = _CHAPTER_IN_PATH.search(path.as_posix())
    if path_match:
        signals.append(int(path_match.group(1)))
    title_match = _CHAPTER_IN_TITLE.search(title)
    if title_match:
        signals.append(int(title_match.group(1)))
    return (signals[0] if signals else None), tuple(dict.fromkeys(signals))


def infer_section(title: str, chapter: int | None) -> str | None:
    match = _SECTION.search(title)
    if not match:
        return None
    value = match.group(1)
    if chapter is not None and not value.startswith(f"{chapter}."):
        return value
    return value


def infer_knowledge_type(title: str, text: str) -> str:
    sample = f"{title}\n{text[:240]}".lower()
    labels = (
        ("definition", ("definition", "定义")),
        ("theorem", ("theorem", "lemma", "proposition", "定理", "引理", "命题")),
        ("proof", ("proof", "证明")),
        ("example", ("example", "例子", "示例")),
        ("exercise", ("exercise", "problem", "练习", "习题")),
    )
    for label, needles in labels:
        if any(needle in sample for needle in needles):
            return label
    return "note"


def _english_terms(text: str) -> tuple[str, ...]:
    terms = re.findall(r"\b[A-Za-z][A-Za-z-]*(?:\s+[A-Za-z][A-Za-z-]*){0,3}\b", text)
    normalized = (normalize_text(term) for term in terms)
    return tuple(dict.fromkeys(term for term in normalized if len(term) > 2))[:20]


def records_from_markdown(
    path: Path,
    *,
    display_path: str,
    source_version: str,
    authority: str = "user_note",
    mirror_paths: Iterable[str] = (),
    topic_expectations: Mapping[str, Mapping[str, object]] | None = None,
) -> tuple[list[SourceRecord], list[KnowledgeAtom], list[ReviewItem]]:
    text = path.read_text(encoding="utf-8")
    sections = split_markdown(text, path.stem)
    records: list[SourceRecord] = []
    atoms: list[KnowledgeAtom] = []
    reviews: list[ReviewItem] = []

    for item in sections:
        chapter, chapter_signals = infer_chapter(path, item.title)
        section = infer_section(item.title, chapter)
        locator = SourceLocator(
            path=display_path,
            start_line=item.start_line,
            end_line=item.end_line,
            chapter=chapter,
            section=section,
        )
        digest = stable_hash(normalize_text(item.text))
        source_id = stable_id("src", "markdown", chapter, section, item.heading_path, digest)
        record = SourceRecord(
            source_id=source_id,
            kind="markdown",
            authority=authority,
            title=item.title,
            text=item.text,
            content_sha256=digest,
            locator=locator,
            source_version=source_version,
            mirror_paths=tuple(sorted(set(mirror_paths))),
            metadata={"heading_path": list(item.heading_path)},
        )
        records.append(record)
        atom = KnowledgeAtom(
            claim_id=stable_id("claim", source_id, digest),
            source_id=source_id,
            chapter=chapter,
            section=section,
            knowledge_type=infer_knowledge_type(item.title, item.text),
            statement_zh=item.text,
            english_terms=_english_terms(item.text),
            assumptions=(),
            dependencies=(),
            conclusion=item.title,
            locator=locator,
            source_version=source_version,
            content_sha256=digest,
        )
        atoms.append(atom)

        if len(chapter_signals) > 1:
            reviews.append(
                ReviewItem(
                    review_id=stable_id("review", "chapter-signal-conflict", source_id),
                    reason="chapter_signal_conflict",
                    source_ids=(source_id,),
                    details={"chapter_signals": list(chapter_signals)},
                )
            )
        for keyword, expected in (topic_expectations or {}).items():
            if keyword.casefold() not in item.text.casefold():
                continue
            expected_chapter = expected.get("chapter")
            expected_section = expected.get("section")
            if (expected_chapter is not None and chapter != int(cast(Any, expected_chapter))) or (
                expected_section is not None and section != str(expected_section)
            ):
                reviews.append(
                    ReviewItem(
                        review_id=stable_id("review", "topic-location", source_id, keyword),
                        reason="topic_location_conflict",
                        source_ids=(source_id,),
                        details={
                            "keyword": keyword,
                            "observed_chapter": chapter,
                            "observed_section": section,
                            "expected": dict(expected),
                        },
                    )
                )
    return records, atoms, reviews
