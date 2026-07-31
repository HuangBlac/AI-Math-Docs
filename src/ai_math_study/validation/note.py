"""Aggregate note validation entrypoint."""

from __future__ import annotations

from ai_math_study.domain.notes import NoteIssue
from .latex import validate_latex
from .markdown import validate_markdown


def validate_note(markdown: str) -> tuple[NoteIssue, ...]:
    return (*validate_markdown(markdown), *validate_latex(markdown))


def note_has_errors(issues: tuple[NoteIssue, ...] | list[NoteIssue]) -> bool:
    return any(issue.is_error for issue in issues)

