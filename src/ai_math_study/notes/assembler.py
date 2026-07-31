"""Deterministic fragmentation and assembly for the note-agent DAG."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re

from ai_math_study.domain.notes import NoteFragment, NotePlan, SectionRewrite
from .protection import ProtectionBundle, TOKEN_PATTERN


class NoteAssemblyError(ValueError):
    pass


@dataclass(frozen=True)
class FragmentedNote:
    frontmatter_token: str | None
    title_line: str | None
    existing_title: str | None
    fragments: tuple[NoteFragment, ...]


_H1 = re.compile(r"^#[ \t]+(.+?)[ \t]*#*[ \t]*(?:\r?$)", re.MULTILINE)
_H2 = re.compile(r"^##[ \t]+(.+?)[ \t]*#*[ \t]*(?:\r?$)", re.MULTILINE)
_TOP_HEADING = re.compile(r"^#{1,2}[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)


def _fragment_id(index: int, markdown: str) -> str:
    digest = sha256(markdown.replace("\r\n", "\n").encode("utf-8")).hexdigest()[:12]
    return f"fragment-{index:03d}-{digest}"


def _heading_text(raw: str) -> str:
    value = raw.strip()
    value = re.sub(r"[ \t]+#+[ \t]*$", "", value)
    return value.strip()


def fragment_protected_note(protected_text: str, bundle: ProtectionBundle) -> FragmentedNote:
    """Split a protected note into deterministic source fragments.

    Frontmatter and the first H1 stay under assembler ownership. H2 sections become
    fragment boundaries; their original heading remains in the fragment so a worker
    can understand the local context, then the assembler removes top-level headings.
    """

    body = protected_text
    frontmatter = next((block for block in bundle.blocks if block.kind == "frontmatter"), None)
    frontmatter_token: str | None = None
    if frontmatter and body.startswith(frontmatter.token):
        frontmatter_token = frontmatter.token
        body = body[len(frontmatter.token) :]

    title_line: str | None = None
    existing_title: str | None = None
    title_match = _H1.search(body)
    if title_match:
        title_line = title_match.group(0).rstrip("\r")
        existing_title = _heading_text(title_match.group(1))
        body = body[: title_match.start()] + body[title_match.end() :]

    matches = list(_H2.finditer(body))
    fragments: list[NoteFragment] = []

    def append_fragment(raw: str, heading_hint: str | None) -> None:
        value = raw.strip()
        if not value:
            return
        index = len(fragments) + 1
        fragments.append(NoteFragment(_fragment_id(index, value), value, heading_hint))

    if not matches:
        append_fragment(body, "正文")
    else:
        append_fragment(body[: matches[0].start()], "导言")
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            append_fragment(body[match.start() : end], _heading_text(match.group(1)))

    if not fragments:
        fragments.append(NoteFragment(_fragment_id(1, ""), "", "正文"))
    return FragmentedNote(frontmatter_token, title_line, existing_title, tuple(fragments))


def _safe_heading(value: str, *, label: str) -> str:
    heading = value.strip().splitlines()[0] if value.strip() else ""
    heading = heading.lstrip("#").strip()
    if not heading:
        raise NoteAssemblyError(f"{label} must be a non-empty single-line heading")
    return heading


def _clean_worker_body(markdown: str) -> str:
    def replace(match: re.Match[str]) -> str:
        content = _heading_text(match.group(1))
        # Never delete a protected token that happened to be embedded in a heading.
        return content if TOKEN_PATTERN.search(content) else ""

    return _TOP_HEADING.sub(replace, markdown).strip()


def assemble_protected_note(
    structure: FragmentedNote,
    plan: NotePlan,
    rewrites: tuple[SectionRewrite, ...],
) -> str:
    rewrite_by_id = {rewrite.section_id: rewrite for rewrite in rewrites}
    if len(rewrite_by_id) != len(rewrites):
        raise NoteAssemblyError("section rewrite ids must be unique")
    expected = {section.section_id for section in plan.sections}
    if set(rewrite_by_id) != expected:
        missing = sorted(expected - set(rewrite_by_id))
        extra = sorted(set(rewrite_by_id) - expected)
        raise NoteAssemblyError(f"section rewrite mismatch; missing={missing}, extra={extra}")

    parts: list[str] = []
    if structure.frontmatter_token:
        parts.append(structure.frontmatter_token)
    if structure.title_line:
        parts.append(structure.title_line)
    else:
        parts.append(f"# {_safe_heading(plan.document_title, label='document_title')}")

    for section in plan.sections:
        parts.append(f"## {_safe_heading(section.heading, label=section.section_id)}")
        body = _clean_worker_body(rewrite_by_id[section.section_id].body_markdown)
        if body:
            parts.append(body)
    return "\n\n".join(part.rstrip() for part in parts if part is not None).rstrip() + "\n"

