"""Lossless protection for Markdown regions that models must not rewrite."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re

from ai_math_study.domain.notes import NoteIssue


TOKEN_PATTERN = re.compile(r"@@AIMATH_[A-Z_]+_\d{4}_[0-9a-f]{12}@@")


class ProtectedTokenError(ValueError):
    pass


@dataclass(frozen=True)
class ProtectedBlock:
    token: str
    kind: str
    content: str
    content_sha256: str
    ordinal: int


@dataclass(frozen=True)
class ProtectionBundle:
    protected_text: str
    blocks: tuple[ProtectedBlock, ...]

    @property
    def tokens(self) -> tuple[str, ...]:
        return tuple(block.token for block in self.blocks)

    def block_by_token(self) -> dict[str, ProtectedBlock]:
        return {block.token: block for block in self.blocks}


def _is_escaped(text: str, index: int) -> bool:
    slashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slashes += 1
        cursor -= 1
    return bool(slashes % 2)


def _find_unescaped(text: str, needle: str, start: int, *, single_dollar: bool = False) -> int:
    cursor = start
    while True:
        index = text.find(needle, cursor)
        if index < 0:
            return -1
        if _is_escaped(text, index):
            cursor = index + len(needle)
            continue
        if single_dollar and (
            (index > 0 and text[index - 1] == "$")
            or (index + 1 < len(text) and text[index + 1] == "$")
        ):
            cursor = index + 1
            continue
        return index


def _frontmatter_end(text: str) -> int | None:
    opener = re.match(r"\A(?:\ufeff)?---[ \t]*(?:\r?\n)", text)
    if not opener:
        return None
    closing = re.search(r"^---[ \t]*(?:\r?\n|\Z)", text[opener.end() :], re.MULTILINE)
    if not closing:
        return None
    return opener.end() + closing.end()


def _fenced_code_end(text: str, start: int) -> int | None:
    if start and text[start - 1] not in "\r\n":
        return None
    opener = re.match(r" {0,3}(`{3,}|~{3,})[^\r\n]*(?:\r?\n|\Z)", text[start:])
    if not opener:
        return None
    marker = opener.group(1)
    search_from = start + opener.end()
    close_pattern = re.compile(
        rf"^ {{0,3}}{re.escape(marker[0])}{{{len(marker)},}}[ \t]*(?:\r?\n|\Z)",
        re.MULTILINE,
    )
    closing = close_pattern.search(text, search_from)
    return closing.end() if closing else len(text)


def protect_markdown(markdown: str) -> ProtectionBundle:
    """Replace protected regions with unique content-addressed sentinels.

    The scanner is precedence-aware: frontmatter and fenced code are consumed before
    inline code, wikilinks, or math can be interpreted inside them.
    """

    blocks: list[ProtectedBlock] = []
    output: list[str] = []
    cursor = 0
    frontmatter_end = _frontmatter_end(markdown)

    def protect(kind: str, start: int, end: int) -> None:
        content = markdown[start:end]
        digest = sha256(content.encode("utf-8")).hexdigest()
        ordinal = len(blocks)
        token = f"@@AIMATH_{kind.upper()}_{ordinal:04d}_{digest[:12]}@@"
        blocks.append(ProtectedBlock(token, kind, content, digest, ordinal))
        output.append(token)

    while cursor < len(markdown):
        if cursor == 0 and frontmatter_end is not None:
            protect("frontmatter", cursor, frontmatter_end)
            cursor = frontmatter_end
            continue

        fence_end = _fenced_code_end(markdown, cursor)
        if fence_end is not None:
            protect("fenced_code", cursor, fence_end)
            cursor = fence_end
            continue

        if markdown[cursor] == "`":
            run = 1
            while cursor + run < len(markdown) and markdown[cursor + run] == "`":
                run += 1
            marker = "`" * run
            end = markdown.find(marker, cursor + run)
            if end >= 0:
                protect("inline_code", cursor, end + run)
                cursor = end + run
                continue

        if markdown.startswith("[[", cursor):
            end = markdown.find("]]", cursor + 2)
            if end >= 0:
                protect("wikilink", cursor, end + 2)
                cursor = end + 2
                continue

        if markdown.startswith("$$", cursor) and not _is_escaped(markdown, cursor):
            end = _find_unescaped(markdown, "$$", cursor + 2)
            if end >= 0:
                protect("block_math", cursor, end + 2)
                cursor = end + 2
                continue

        if markdown.startswith(r"\[", cursor) and not _is_escaped(markdown, cursor):
            end = _find_unescaped(markdown, r"\]", cursor + 2)
            if end >= 0:
                protect("block_math", cursor, end + 2)
                cursor = end + 2
                continue

        if markdown.startswith(r"\(", cursor) and not _is_escaped(markdown, cursor):
            end = _find_unescaped(markdown, r"\)", cursor + 2)
            if end >= 0:
                protect("inline_math", cursor, end + 2)
                cursor = end + 2
                continue

        if markdown[cursor] == "$" and not _is_escaped(markdown, cursor):
            if not markdown.startswith("$$", cursor):
                end = _find_unescaped(markdown, "$", cursor + 1, single_dollar=True)
                newline = markdown.find("\n", cursor + 1)
                if end >= 0 and (newline < 0 or end < newline):
                    protect("inline_math", cursor, end + 1)
                    cursor = end + 1
                    continue

        output.append(markdown[cursor])
        cursor += 1

    return ProtectionBundle("".join(output), tuple(blocks))


def validate_token_bijection(protected_text: str, bundle: ProtectionBundle) -> tuple[NoteIssue, ...]:
    issues: list[NoteIssue] = []
    expected = set(bundle.tokens)
    for block in bundle.blocks:
        count = protected_text.count(block.token)
        if count == 0:
            issues.append(
                NoteIssue("error", "protected_token_missing", f"Protected token is missing: {block.token}", token=block.token)
            )
        elif count > 1:
            issues.append(
                NoteIssue(
                    "error",
                    "protected_token_duplicate",
                    f"Protected token occurs {count} times: {block.token}",
                    token=block.token,
                )
            )
    unknown = sorted(set(TOKEN_PATTERN.findall(protected_text)) - expected)
    for token in unknown:
        issues.append(NoteIssue("error", "protected_token_unknown", f"Unknown protected token: {token}", token=token))
    return tuple(issues)


def restore_markdown(protected_text: str, bundle: ProtectionBundle) -> str:
    issues = validate_token_bijection(protected_text, bundle)
    if issues:
        kinds = {issue.code for issue in issues}
        if "protected_token_missing" in kinds:
            label = "missing"
        elif "protected_token_duplicate" in kinds:
            label = "duplicate"
        else:
            label = "unknown"
        raise ProtectedTokenError(f"Protected token {label}: {issues[0].message}")
    restored = protected_text
    for block in bundle.blocks:
        restored = restored.replace(block.token, block.content)
    leftovers = TOKEN_PATTERN.findall(restored)
    if leftovers:
        raise ProtectedTokenError(f"Unrestored protected token: {leftovers[0]}")
    return restored

