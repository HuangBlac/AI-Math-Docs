"""Fail-closed detection of active constructs newly introduced by organize."""

from __future__ import annotations

from collections import Counter
import re

from ai_math_study.domain.notes import NoteIssue


_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("raw_html", re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>", re.IGNORECASE)),
    ("remote_url", re.compile(r"https?://[^\s<>'\")\]]+", re.IGNORECASE)),
    ("mkdocs_snippet", re.compile(r"--8<--\s*(?:\"[^\"]+\"|'[^']+'|\S+)", re.IGNORECASE)),
    ("template_include", re.compile(r"{[%{]\s*(?:include|import)\b.*?[}%]}", re.IGNORECASE)),
    ("event_attribute", re.compile(r"\bon[a-z]+\s*=", re.IGNORECASE)),
    ("script_scheme", re.compile(r"\b(?:javascript|vbscript|data)\s*:", re.IGNORECASE)),
)


def _inventory(markdown: str) -> Counter[tuple[str, str]]:
    found: Counter[tuple[str, str]] = Counter()
    for kind, pattern in _PATTERNS:
        for match in pattern.finditer(markdown):
            found[(kind, match.group(0))] += 1
    return found


def validate_no_new_active_constructs(original: str, proposed: str) -> tuple[NoteIssue, ...]:
    """Reject constructs not already present, including additional duplicates."""

    before = _inventory(original)
    after = _inventory(proposed)
    issues: list[NoteIssue] = []
    for (kind, value), count in sorted(after.items()):
        introduced = count - before[(kind, value)]
        if introduced > 0:
            excerpt = value.replace("\n", " ")[:100]
            issues.append(
                NoteIssue(
                    severity="error",
                    code="new_active_construct",
                    message=f"organize introduced {introduced} {kind} construct(s): {excerpt}",
                )
            )
    return tuple(issues)
