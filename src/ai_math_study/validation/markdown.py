"""Deterministic Markdown structure checks used before any file mutation."""

from __future__ import annotations

import re

from ai_math_study.domain.notes import NoteIssue
from ai_math_study.notes.protection import TOKEN_PATTERN, protect_markdown


_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})[^\r\n]*(?:\r?\n|\Z)")


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _fence_issues(markdown: str) -> list[NoteIssue]:
    issues: list[NoteIssue] = []
    active_char: str | None = None
    active_length = 0
    active_line = 0
    for line_number, line in enumerate(markdown.splitlines(keepends=True), 1):
        stripped = line.rstrip("\r\n")
        candidate = _FENCE.match(line)
        if active_char is None:
            if candidate:
                marker = candidate.group(1)
                active_char = marker[0]
                active_length = len(marker)
                active_line = line_number
        else:
            closing = re.fullmatch(rf" {{0,3}}{re.escape(active_char)}{{{active_length},}}[ \t]*", stripped)
            if closing:
                active_char = None
                active_length = 0
                active_line = 0
    if active_char is not None:
        issues.append(
            NoteIssue(
                "error",
                "markdown_fence_unbalanced",
                f"Code fence opened on line {active_line} is not closed",
                line=active_line,
            )
        )
    return issues


def _frontmatter_issues(markdown: str) -> list[NoteIssue]:
    value = markdown[1:] if markdown.startswith("\ufeff") else markdown
    if not re.match(r"\A---[ \t]*(?:\r?\n)", value):
        return []
    if not re.search(r"^---[ \t]*(?:\r?\n|\Z)", value.split("\n", 1)[1], re.MULTILINE):
        return [NoteIssue("error", "markdown_frontmatter_unbalanced", "YAML frontmatter is not closed", line=1)]
    return []


def validate_markdown(markdown: str) -> tuple[NoteIssue, ...]:
    issues: list[NoteIssue] = []
    issues.extend(_frontmatter_issues(markdown))
    issues.extend(_fence_issues(markdown))

    for token in sorted(set(TOKEN_PATTERN.findall(markdown))):
        issues.append(
            NoteIssue(
                "error",
                "protected_token_unresolved",
                f"Unrestored protection token remains in Markdown: {token}",
                line=_line_number(markdown, markdown.find(token)),
                token=token,
            )
        )

    protected = protect_markdown(markdown).protected_text
    headings = list(_HEADING.finditer(protected))
    h1 = [match for match in headings if len(match.group(1)) == 1]
    if len(h1) != 1:
        issues.append(
            NoteIssue(
                "error",
                "markdown_h1_count",
                f"Expected exactly one H1 heading, found {len(h1)}",
                line=_line_number(protected, h1[0].start()) if h1 else None,
            )
        )

    previous_level: int | None = None
    for heading in headings:
        level = len(heading.group(1))
        if previous_level is not None and level > previous_level + 1:
            issues.append(
                NoteIssue(
                    "error",
                    "markdown_heading_jump",
                    f"Heading level jumps from H{previous_level} to H{level}",
                    line=_line_number(protected, heading.start()),
                )
            )
        previous_level = level
    return tuple(issues)

