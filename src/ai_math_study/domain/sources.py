from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Mapping, cast


VERIFICATION_STATES = frozenset(
    {"unverified", "source-aligned", "contradicted", "verified"}
)
SOURCE_AUTHORITIES = frozenset(
    {"primary_text", "user_note", "derived_wiki", "published_copy"}
)
CORPUS_TIERS = frozenset({"core", "prerequisite"})


def canonical_json(value: object) -> str:
    """Return the canonical UTF-8 JSON representation used for all hashes."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def stable_hash(value: bytes | str | object) -> str:
    if isinstance(value, bytes):
        payload = value
    elif isinstance(value, str):
        payload = value.encode("utf-8")
    else:
        payload = canonical_json(value).encode("utf-8")
    return sha256(payload).hexdigest()


def stable_id(prefix: str, *parts: object, length: int = 24) -> str:
    return f"{prefix}_{stable_hash(list(parts))[:length]}"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


@dataclass(frozen=True)
class SectionAnchor:
    section: str
    title: str
    print_page: int
    pdf_page: int
    depth: int = 1


@dataclass(frozen=True)
class ChapterRange:
    chapter: int
    title: str
    print_start: int
    print_end: int
    pdf_start: int
    pdf_end: int
    sections: tuple[SectionAnchor, ...] = ()

    def __post_init__(self) -> None:
        if self.chapter < 1:
            raise ValueError("chapter must be positive")
        if self.print_start > self.print_end or self.pdf_start > self.pdf_end:
            raise ValueError(f"invalid page range for chapter {self.chapter}")
        if (self.print_end - self.print_start) != (self.pdf_end - self.pdf_start):
            raise ValueError(
                f"print/PDF page ranges have different lengths for chapter {self.chapter}"
            )

    def print_page_for(self, pdf_page: int) -> int:
        if not self.pdf_start <= pdf_page <= self.pdf_end:
            raise ValueError(f"PDF page {pdf_page} is outside chapter {self.chapter}")
        return self.print_start + pdf_page - self.pdf_start

    @classmethod
    def from_spec(cls, value: Mapping[str, Any] | object) -> "ChapterRange":
        if not isinstance(value, Mapping):
            if hasattr(value, "model_dump"):
                value = value.model_dump()
            elif hasattr(value, "__dict__"):
                value = vars(value)
            else:
                raise TypeError(f"unsupported chapter specification: {type(value)!r}")
        row: dict[str, Any] = dict(cast(Mapping[str, Any], value))
        printed = row.get("printed_pages")
        physical = row.get("pdf_pages")
        if printed is not None:
            row.setdefault("print_start", printed[0])
            row.setdefault("print_end", printed[1])
        if physical is not None:
            row.setdefault("pdf_start", physical[0])
            row.setdefault("pdf_end", physical[1])
        aliases = {
            "printed_start": "print_start",
            "printed_end": "print_end",
            "physical_start": "pdf_start",
            "physical_end": "pdf_end",
        }
        for old, new in aliases.items():
            if old in row and new not in row:
                row[new] = row[old]
        sections = tuple(
            SectionAnchor(
                section=str(anchor["section"]),
                title=str(anchor.get("title_en", anchor.get("title", anchor["section"]))),
                print_page=int(cast(Any, anchor.get("printed_page", anchor.get("print_page")))),
                pdf_page=int(anchor["pdf_page"]),
                depth=int(anchor.get("depth", 1)),
            )
            for anchor in (
                item.model_dump() if hasattr(item, "model_dump") else dict(item)
                for item in row.get("sections", ())
            )
        )
        return cls(
            chapter=int(row["chapter"]),
            title=str(row.get("title_en", row.get("title", f"Chapter {row['chapter']}"))),
            print_start=int(row["print_start"]),
            print_end=int(row["print_end"]),
            pdf_start=int(row["pdf_start"]),
            pdf_end=int(row["pdf_end"]),
            sections=sections,
        )


@dataclass(frozen=True)
class CorpusManifest:
    pdf_sha256: str
    pdf_page_count: int
    chapters: tuple[ChapterRange, ...]
    source_version: str = "lftp-local"
    topic_expectations: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "pdf_sha256", self.pdf_sha256.lower())
        if not re.fullmatch(r"[0-9a-f]{64}", self.pdf_sha256):
            raise ValueError("pdf_sha256 must be a 64-character hexadecimal digest")
        if self.pdf_page_count < 1:
            raise ValueError("pdf_page_count must be positive")
        chapter_numbers = [chapter.chapter for chapter in self.chapters]
        if len(chapter_numbers) != len(set(chapter_numbers)):
            raise ValueError("chapter numbers must be unique")
        ordered = sorted(self.chapters, key=lambda item: item.pdf_start)
        for left, right in zip(ordered, ordered[1:]):
            if left.pdf_end >= right.pdf_start:
                raise ValueError("chapter PDF page ranges overlap")
        if any(chapter.pdf_end > self.pdf_page_count for chapter in self.chapters):
            raise ValueError("chapter page range exceeds pdf_page_count")

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CorpusManifest":
        pdf = data.get("pdf", {}) if isinstance(data.get("pdf"), Mapping) else {}
        sha = data.get("pdf_sha256", pdf.get("sha256"))
        count = data.get("pdf_page_count", pdf.get("page_count"))
        raw_chapters = data.get("chapters", ())
        chapters: list[ChapterRange] = []
        if isinstance(raw_chapters, Mapping):
            iterable: Iterable[tuple[Any, Any]] = raw_chapters.items()
        else:
            iterable = ((None, item) for item in raw_chapters)
        for key, item in iterable:
            row = item.model_dump() if hasattr(item, "model_dump") else dict(item)
            row.setdefault("chapter", key)
            chapters.append(ChapterRange.from_spec(row))
        if sha is None or count is None:
            raise ValueError("manifest must contain PDF sha256 and page_count")
        return cls(
            pdf_sha256=str(sha),
            pdf_page_count=int(count),
            chapters=tuple(sorted(chapters, key=lambda item: item.chapter)),
            source_version=str(data.get("source_version", "lftp-local")),
            topic_expectations=data.get("topic_expectations", {}),
        )

    @classmethod
    def coerce(cls, value: "CorpusManifest | Mapping[str, Any] | str | Path | object") -> "CorpusManifest":
        if isinstance(value, cls):
            return value
        if isinstance(value, (str, Path)):
            return cls.load(value)
        if not isinstance(value, Mapping):
            if hasattr(value, "model_dump"):
                value = value.model_dump()
            else:
                raise TypeError(f"unsupported corpus manifest: {type(value)!r}")
        row = dict(cast(Mapping[str, Any], value))
        # Native Syllabus uses source_sha256/page_count and ChapterSpec page pairs.
        if "source_sha256" in row:
            row.setdefault("pdf_sha256", row["source_sha256"])
        if "page_count" in row:
            row.setdefault("pdf_page_count", row["page_count"])
        return cls.from_dict(row)

    @classmethod
    def load(cls, path: str | Path) -> "CorpusManifest":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_dict(self) -> dict[str, Any]:
        return {
            "pdf_sha256": self.pdf_sha256,
            "pdf_page_count": self.pdf_page_count,
            "source_version": self.source_version,
            "chapters": [asdict(chapter) for chapter in self.chapters],
            "topic_expectations": dict(self.topic_expectations),
        }


@dataclass(frozen=True)
class SourceLocator:
    path: str
    start_line: int | None = None
    end_line: int | None = None
    pdf_page: int | None = None
    print_page: int | None = None
    chapter: int | None = None
    section: str | None = None
    bbox: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    kind: str
    authority: str
    title: str
    text: str
    content_sha256: str
    locator: SourceLocator
    source_version: str
    mirror_paths: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    corpus_tier: str = "core"
    verification_state: str = "unverified"

    def __post_init__(self) -> None:
        if self.authority not in SOURCE_AUTHORITIES:
            raise ValueError(f"invalid source authority: {self.authority}")
        if self.corpus_tier not in CORPUS_TIERS:
            raise ValueError(f"invalid corpus tier: {self.corpus_tier}")
        if self.verification_state not in VERIFICATION_STATES:
            raise ValueError(f"invalid verification state: {self.verification_state}")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["metadata"] = dict(self.metadata)
        return value


@dataclass(frozen=True)
class KnowledgeAtom:
    claim_id: str
    source_id: str
    chapter: int | None
    section: str | None
    knowledge_type: str
    statement_zh: str
    english_terms: tuple[str, ...]
    assumptions: tuple[str, ...]
    dependencies: tuple[str, ...]
    conclusion: str
    locator: SourceLocator
    source_version: str
    content_sha256: str
    verification_state: str = "unverified"
    misconception_tags: tuple[str, ...] = ()
    evidence_type: str = "extracted_text"
    formula_uncertain: bool = False

    def __post_init__(self) -> None:
        if self.verification_state not in VERIFICATION_STATES:
            raise ValueError(f"invalid verification state: {self.verification_state}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewItem:
    review_id: str
    reason: str
    source_ids: tuple[str, ...]
    details: Mapping[str, Any]
    status: str = "open"

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["details"] = dict(self.details)
        return value
