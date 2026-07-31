"""Conservative LaTeX delimiter and environment validation.

This is a syntax guard, not a theorem prover and not a full TeX implementation.
It intentionally checks only invariants that can be established deterministically.
"""

from __future__ import annotations

import re

from ai_math_study.domain.notes import NoteIssue
from ai_math_study.notes.protection import ProtectionBundle, protect_markdown


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _is_escaped(text: str, index: int) -> bool:
    count = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        count += 1
        cursor -= 1
    return bool(count % 2)


def _math_body(content: str) -> str:
    if content.startswith("$$") and content.endswith("$$"):
        return content[2:-2]
    if content.startswith("$") and content.endswith("$"):
        return content[1:-1]
    if content.startswith(r"\[") and content.endswith(r"\]"):
        return content[2:-2]
    if content.startswith(r"\(") and content.endswith(r"\)"):
        return content[2:-2]
    return content


def _balanced_braces(text: str) -> bool:
    depth = 0
    for index, char in enumerate(text):
        if char == "{" and not _is_escaped(text, index):
            depth += 1
        elif char == "}" and not _is_escaped(text, index):
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def _environment_issues(body: str, token: str) -> list[NoteIssue]:
    issues: list[NoteIssue] = []
    stack: list[str] = []
    for match in re.finditer(r"\\(begin|end)\{([^{}]+)\}", body):
        operation, environment = match.groups()
        if operation == "begin":
            stack.append(environment)
        elif not stack or stack[-1] != environment:
            expected = stack[-1] if stack else None
            suffix = f"; expected \\end{{{expected}}}" if expected else ""
            issues.append(
                NoteIssue(
                    "error",
                    "latex_environment",
                    f"Unmatched \\end{{{environment}}}{suffix}",
                    token=token,
                )
            )
            if stack:
                stack.pop()
        else:
            stack.pop()
    for environment in reversed(stack):
        issues.append(
            NoteIssue(
                "error",
                "latex_environment",
                f"Missing \\end{{{environment}}}",
                token=token,
            )
        )
    return issues


def _unmatched_delimiter_issues(markdown: str, bundle: ProtectionBundle) -> list[NoteIssue]:
    residual = bundle.protected_text
    issues: list[NoteIssue] = []

    dollar_index = next(
        (
            index
            for index, char in enumerate(residual)
            if char == "$" and not _is_escaped(residual, index)
        ),
        None,
    )
    if dollar_index is not None:
        issues.append(
            NoteIssue(
                "error",
                "latex_dollar_unbalanced",
                "Unbalanced dollar math delimiter",
                line=_line_number(residual, dollar_index),
            )
        )

    for opener, closer, code in (
        (r"\[", r"\]", "latex_bracket_unbalanced"),
        (r"\(", r"\)", "latex_parenthesis_unbalanced"),
    ):
        for needle in (opener, closer):
            index = residual.find(needle)
            if index >= 0 and not _is_escaped(residual, index):
                issues.append(
                    NoteIssue(
                        "error",
                        code,
                        f"Unbalanced math delimiter {needle}",
                        line=_line_number(residual, index),
                    )
                )
                break
    return issues


def validate_latex(markdown: str) -> tuple[NoteIssue, ...]:
    bundle = protect_markdown(markdown)
    issues = _unmatched_delimiter_issues(markdown, bundle)
    for block in bundle.blocks:
        if block.kind not in {"inline_math", "block_math"}:
            continue
        body = _math_body(block.content)
        left_count = len(re.findall(r"\\left\b", body))
        right_count = len(re.findall(r"\\right\b", body))
        if left_count != right_count:
            issues.append(
                NoteIssue(
                    "error",
                    "latex_left_right",
                    f"Unbalanced \\left and \\right ({left_count} vs {right_count})",
                    token=block.token,
                )
            )
        if not _balanced_braces(body):
            issues.append(NoteIssue("error", "latex_braces", "Unbalanced LaTeX braces", token=block.token))
        issues.extend(_environment_issues(body, block.token))
    return tuple(issues)

