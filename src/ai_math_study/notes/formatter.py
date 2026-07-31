"""Deterministic, content-conserving Markdown format operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .scanner import ScannedDocument, scan_utf8


class FormatError(ValueError):
    """Raised when conservation cannot be proven."""


@dataclass(frozen=True)
class FormatOperation:
    kind: Literal["heading", "list_item", "whitespace"]
    line: int = 0
    value: int | None = None
    start: int | None = None
    end: int | None = None
    replacement: bytes | None = None

    @classmethod
    def heading(cls, *, line: int, level: int) -> FormatOperation:
        if not 1 <= level <= 6:
            raise FormatError("heading level must be between 1 and 6")
        return cls("heading", line, level)

    @classmethod
    def list_item(cls, *, line: int) -> FormatOperation:
        return cls("list_item", line)

    @classmethod
    def replace_whitespace(cls, *, start: int, end: int, replacement: bytes) -> FormatOperation:
        """Replace one explicit byte span, provided both sides are whitespace-only."""

        return cls("whitespace", start=start, end=end, replacement=replacement)


def _line_ranges(data: bytes) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    start = 0
    for raw in data.splitlines(keepends=True):
        result.append((start, start + len(raw)))
        start += len(raw)
    if start < len(data) or not result:
        result.append((start, len(data)))
    return result


def _prefix(operation: FormatOperation) -> bytes:
    if operation.kind == "heading":
        assert operation.value is not None
        return b"#" * operation.value + b" "
    return b"- "


def _validate_target(document: ScannedDocument, operation: FormatOperation, ranges: list[tuple[int, int]]) -> int:
    if operation.line < 1 or operation.line > len(ranges):
        raise FormatError(f"line {operation.line} is outside the document")
    start, end = ranges[operation.line - 1]
    if start == end or document.data[start:end].strip(b"\r\n \t") == b"":
        raise FormatError("cannot attach a marker to an empty line")
    if any(start < span.end and end > span.start for span in document.protected):
        raise FormatError(f"line {operation.line} intersects protected content")
    return start


def format_utf8(data: bytes, operations: tuple[FormatOperation, ...]) -> bytes:
    """Apply only provenance-tracked markers and prove the content ledger unchanged."""

    if not operations:
        return data
    before = scan_utf8(data)
    ranges = _line_ranges(data)
    edits: list[tuple[int, int, bytes]] = []
    used_lines: set[int] = set()
    for operation in operations:
        if operation.kind == "whitespace":
            if operation.start is None or operation.end is None or operation.replacement is None:
                raise FormatError("whitespace operation requires start, end, and replacement")
            start, end = operation.start, operation.end
            if not 0 <= start <= end <= len(data):
                raise FormatError("whitespace byte span is outside the document")
            if data[start:end].strip() or operation.replacement.strip():
                raise FormatError("whitespace operation may contain whitespace bytes only")
            if any(
                (start < span.end and end > span.start)
                or (start == end and span.start < start < span.end)
                for span in before.protected
            ):
                raise FormatError("whitespace operation intersects protected content")
            edits.append((start, end, operation.replacement))
            continue
        if operation.line in used_lines:
            raise FormatError("at most one format operation is allowed per line")
        offset = _validate_target(before, operation, ranges)
        edits.append((offset, offset, _prefix(operation)))
        used_lines.add(operation.line)

    chunks: list[bytes] = []
    cursor = 0
    for start, end, replacement in sorted(edits):
        if start < cursor:
            raise FormatError("format operations overlap")
        chunks.extend((data[cursor:start], replacement))
        cursor = end
    chunks.append(data[cursor:])
    result = b"".join(chunks)
    after = scan_utf8(result)
    if before.ledger != after.ledger:
        raise FormatError("content ledger changed; refusing format result")
    before_protected = tuple((span.kind, data[span.start : span.end]) for span in before.protected)
    after_protected = tuple((span.kind, result[span.start : span.end]) for span in after.protected)
    if before_protected != after_protected:
        raise FormatError("protected formula/code/content changed; refusing format result")
    return result


def paste_preview(data: bytes, operations: tuple[FormatOperation, ...] = ()) -> bytes:
    """Pure in-memory entry point for clipboard/stdin callers."""

    return format_utf8(data, operations)
