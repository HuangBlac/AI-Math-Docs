from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence, cast

from ai_math_study.domain.sources import (
    CorpusManifest,
    KnowledgeAtom,
    ReviewItem,
    SourceRecord,
    canonical_json,
    normalize_text,
    stable_id,
)

from .markdown import records_from_markdown
from .pdf import DefaultPDFExtractor, PDFExtractor, records_from_pdf
from .generation import publish_generation
from .store import (
    artifact_descriptor,
    build_sqlite,
    file_sha256,
    stable_manifest_digest,
    write_if_changed,
    write_jsonl,
)


@dataclass(frozen=True)
class IngestConfig:
    project_root: Path
    pdf_path: Path
    manifest: CorpusManifest | Path | Mapping[str, object] | object
    markdown_roots: tuple[Path, ...]
    study_dir: Path
    chapters: tuple[int | Mapping[str, object] | object, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    pdf_extractor: PDFExtractor | None = None


@dataclass(frozen=True)
class BuildResult:
    study_dir: Path
    manifest_path: Path
    database_path: Path
    source_count: int
    atom_count: int
    review_count: int
    deduplicated_file_count: int
    manifest_sha256: str


def _display_path(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _markdown_files(roots: Iterable[Path]) -> list[Path]:
    files: set[Path] = set()
    for root in roots:
        if root.is_file() and root.suffix.lower() in {".md", ".markdown"}:
            files.add(root.resolve())
        elif root.exists():
            files.update(
                path.resolve()
                for path in root.rglob("*")
                if path.is_file() and path.suffix.lower() in {".md", ".markdown"}
            )
    return sorted(files, key=lambda path: path.as_posix().casefold())


def _deduplicate_records(
    sources: Sequence[SourceRecord], atoms: Sequence[KnowledgeAtom]
) -> tuple[list[SourceRecord], list[KnowledgeAtom]]:
    chosen_sources: dict[str, SourceRecord] = {}
    source_alias: dict[str, str] = {}
    semantic: dict[tuple[object, ...], str] = {}
    for source in sorted(sources, key=lambda item: (item.source_id, item.locator.path)):
        key = (
            source.kind,
            source.locator.chapter,
            source.locator.section,
            normalize_text(source.title).casefold(),
            source.content_sha256,
        )
        existing_id = semantic.get(key)
        if existing_id is None:
            semantic[key] = source.source_id
            chosen_sources[source.source_id] = source
            source_alias[source.source_id] = source.source_id
            continue
        source_alias[source.source_id] = existing_id
        existing = chosen_sources[existing_id]
        mirrors = tuple(
            sorted(
                set(existing.mirror_paths)
                | set(source.mirror_paths)
                | {source.locator.path}
            )
        )
        chosen_sources[existing_id] = replace(existing, mirror_paths=mirrors)

    chosen_atoms: dict[str, KnowledgeAtom] = {}
    for atom in sorted(atoms, key=lambda item: item.claim_id):
        canonical_source = source_alias.get(atom.source_id, atom.source_id)
        canonical_atom = atom
        if canonical_source != atom.source_id:
            canonical_atom = replace(
                atom,
                source_id=canonical_source,
                claim_id=stable_id("claim", canonical_source, atom.content_sha256),
            )
        chosen_atoms.setdefault(canonical_atom.claim_id, canonical_atom)
    return (
        sorted(chosen_sources.values(), key=lambda item: item.source_id),
        sorted(chosen_atoms.values(), key=lambda item: item.claim_id),
    )


def _content_conflicts(sources: Sequence[SourceRecord]) -> list[ReviewItem]:
    grouped: dict[tuple[object, ...], list[SourceRecord]] = {}
    for source in sources:
        if source.kind != "markdown":
            continue
        key = (
            source.locator.chapter,
            source.locator.section,
            normalize_text(source.title).casefold(),
        )
        grouped.setdefault(key, []).append(source)
    reviews: list[ReviewItem] = []
    for conflict_key, candidates in sorted(grouped.items(), key=lambda item: repr(item[0])):
        hashes = {candidate.content_sha256 for candidate in candidates}
        if len(hashes) <= 1:
            continue
        source_ids = tuple(sorted(candidate.source_id for candidate in candidates))
        reviews.append(
            ReviewItem(
                review_id=stable_id("review", "source-content-conflict", conflict_key, source_ids),
                reason="source_content_conflict",
                source_ids=source_ids,
                details={
                    "chapter": conflict_key[0],
                    "section": conflict_key[1],
                    "title": conflict_key[2],
                    "content_sha256": sorted(hashes),
                },
            )
        )
    return reviews


def build_corpus(config: IngestConfig) -> BuildResult:
    root = config.project_root.resolve()
    pdf_path = config.pdf_path.resolve()
    manifest = CorpusManifest.coerce(config.manifest)

    def chapter_number(value: int | Mapping[str, object] | object) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, Mapping):
            return int(cast(Any, value["chapter"]))
        return int(cast(Any, getattr(value, "chapter")))

    selected = tuple(sorted({chapter_number(value) for value in config.chapters}))
    available = {chapter.chapter: chapter for chapter in manifest.chapters}
    missing = [chapter for chapter in selected if chapter not in available]
    if missing:
        raise ValueError(f"chapters absent from external manifest: {missing}")
    actual_pdf_hash = file_sha256(pdf_path)
    if actual_pdf_hash != manifest.pdf_sha256:
        raise ValueError(
            f"PDF SHA-256 mismatch: expected {manifest.pdf_sha256}, got {actual_pdf_hash}"
        )
    extractor = config.pdf_extractor or DefaultPDFExtractor()
    actual_pages = extractor.page_count(pdf_path)
    if actual_pages != manifest.pdf_page_count:
        raise ValueError(
            f"PDF page count mismatch: expected {manifest.pdf_page_count}, got {actual_pages}"
        )

    source_records, atoms = records_from_pdf(
        pdf_path,
        display_path=_display_path(pdf_path, root),
        chapters=[available[chapter] for chapter in selected],
        source_version=manifest.pdf_sha256,
        extractor=extractor,
    )
    reviews: list[ReviewItem] = []
    markdown_paths = _markdown_files(config.markdown_roots)
    input_rows: list[dict[str, str]] = [
        {"path": _display_path(pdf_path, root), "sha256": actual_pdf_hash}
    ]
    files_by_hash: dict[str, list[Path]] = {}
    for path in markdown_paths:
        digest = file_sha256(path)
        input_rows.append({"path": _display_path(path, root), "sha256": digest})
        files_by_hash.setdefault(digest, []).append(path)

    duplicate_count = 0
    authority_order = {"user_note": 0, "derived_wiki": 1}
    for digest, paths in sorted(files_by_hash.items()):
        ranked = sorted(
            paths,
            key=lambda path: (
                authority_order[
                    "derived_wiki" if "wiki" in path.parts else "user_note"
                ],
                _display_path(path, root).casefold(),
            ),
        )
        representative = ranked[0]
        mirrors = tuple(_display_path(path, root) for path in ranked[1:])
        duplicate_count += len(mirrors)
        authority = "derived_wiki" if "wiki" in representative.parts else "user_note"
        md_sources, md_atoms, md_reviews = records_from_markdown(
            representative,
            display_path=_display_path(representative, root),
            source_version=digest,
            authority=authority,
            mirror_paths=mirrors,
            topic_expectations=manifest.topic_expectations,
        )
        source_records.extend(md_sources)
        atoms.extend(md_atoms)
        reviews.extend(md_reviews)

    reviews.extend(_content_conflicts(source_records))
    source_records, atoms = _deduplicate_records(source_records, atoms)
    reviews_by_id = {review.review_id: review for review in reviews}
    reviews = sorted(reviews_by_id.values(), key=lambda item: item.review_id)

    study_root = config.study_dir.resolve()
    study_root.mkdir(parents=True, exist_ok=True)
    import tempfile

    staging = Path(tempfile.mkdtemp(prefix=".corpus-", dir=study_root))
    sources_path = staging / "sources.jsonl"
    atoms_path = staging / "atoms.jsonl"
    reviews_path = staging / "review_queue.jsonl"
    database_path = staging / "corpus.sqlite3"
    write_jsonl(sources_path, (item.to_dict() for item in source_records))
    write_jsonl(atoms_path, (item.to_dict() for item in atoms))
    write_jsonl(reviews_path, (item.to_dict() for item in reviews))

    output_manifest: dict[str, object] = {
        "schema_version": 2,
        "extractor_version": "aimath-pdf-v1",
        "canonicalizer_version": "aimath-text-v1",
        "source_spec": manifest.to_dict(),
        "selected_chapters": list(selected),
        "inputs": sorted(input_rows, key=lambda item: item["path"].casefold()),
        "deduplicated_file_count": duplicate_count,
        "artifacts": {
            "sources": artifact_descriptor(sources_path, len(source_records)),
            "atoms": artifact_descriptor(atoms_path, len(atoms)),
            "review_queue": artifact_descriptor(reviews_path, len(reviews)),
        },
    }
    manifest_digest = stable_manifest_digest(output_manifest)
    build_sqlite(
        database_path,
        source_records,
        atoms,
        reviews,
        manifest_sha256=manifest_digest,
    )
    manifest_path = staging / "manifest.json"
    write_if_changed(
        manifest_path,
        (canonical_json(output_manifest) + "\n").encode("utf-8"),
    )
    generation = publish_generation(study_root, staging, "gen-" + manifest_digest)
    return BuildResult(
        study_dir=generation,
        manifest_path=generation / "manifest.json",
        database_path=generation / "corpus.sqlite3",
        source_count=len(source_records),
        atom_count=len(atoms),
        review_count=len(reviews),
        deduplicated_file_count=duplicate_count,
        manifest_sha256=manifest_digest,
    )
