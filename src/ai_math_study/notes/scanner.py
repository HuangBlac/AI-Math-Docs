"""Conservative UTF-8 byte-span scanner for lossless note formatting."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re


class ScanError(ValueError):
    """Raised when a document cannot be parsed without guessing."""


@dataclass(frozen=True)
class ByteSpan:
    start: int
    end: int
    kind: str
    digest: str


@dataclass(frozen=True)
class ScannedDocument:
    data: bytes
    protected: tuple[ByteSpan, ...]
    ledger: tuple[str, ...]


_FENCE = re.compile(r"(?m)^(?P<mark>`{3,}|~{3,})[^\r\n]*(?:\r?\n)")
_INLINE = re.compile(r"`[^`\r\n]+`")
_WIKILINK = re.compile(r"\[\[[^\]\r\n]+\]\]")
_URL = re.compile(r"https?://[^\s<>]+")
_BLOCK_MATH = re.compile(r"\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]")
_INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)[^$\r\n]+(?<!\\)\$")
_LINE_MARKER = re.compile(rb"(?m)^(?:[ \t]{0,3})(?:#{1,6}[ \t]+|[-+*][ \t]+|\d+[.)][ \t]+)")


def _byte_offsets(text: str) -> list[int]:
    offsets = [0]
    total = 0
    for char in text:
        total += len(char.encode("utf-8"))
        offsets.append(total)
    return offsets


def _span(text: str, offsets: list[int], start: int, end: int, kind: str) -> ByteSpan:
    raw = text[start:end].encode("utf-8")
    return ByteSpan(offsets[start], offsets[end], kind, sha256(raw).hexdigest())


def _fenced_spans(text: str, offsets: list[int]) -> list[ByteSpan]:
    spans: list[ByteSpan] = []
    cursor = 0
    while match := _FENCE.search(text, cursor):
        mark = re.escape(match.group("mark"))
        closing = re.compile(rf"(?m)^[ \t]{{0,3}}{mark}[ \t]*(?:\r?$)").search(text, match.end())
        if closing is None:
            raise ScanError("unterminated fenced code block")
        end = closing.end()
        spans.append(_span(text, offsets, match.start(), end, "code_fence"))
        cursor = end
    return spans


def _inside(spans: list[ByteSpan], start: int, end: int) -> bool:
    return any(start < span.end and end > span.start for span in spans)


def scan_utf8(data: bytes) -> ScannedDocument:
    """Scan valid UTF-8, rejecting constructs whose boundaries are ambiguous."""

    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ScanError("input must be valid UTF-8") from exc
    if text.startswith("\ufeff"):
        raise ScanError("UTF-8 BOM is not accepted in strict format mode")
    offsets = _byte_offsets(text)
    spans = _fenced_spans(text, offsets)

    if text.startswith("---\n") or text.startswith("---\r\n"):
        opening_end = text.index("\n") + 1
        closing = re.search(r"(?m)^---[ \t]*\r?$", text[opening_end:])
        if closing is None:
            raise ScanError("unterminated frontmatter")
        end = opening_end + closing.end()
        spans.append(_span(text, offsets, 0, end, "frontmatter"))

    patterns = (
        ("math", _BLOCK_MATH),
        ("inline_code", _INLINE),
        ("wikilink", _WIKILINK),
        ("url", _URL),
        ("math", _INLINE_MATH),
    )
    for kind, pattern in patterns:
        for match in pattern.finditer(text):
            start, end = offsets[match.start()], offsets[match.end()]
            if not _inside(spans, start, end):
                spans.append(_span(text, offsets, match.start(), match.end(), kind))

    # Any remaining unescaped dollar is ambiguous rather than assumed to be prose.
    masked = bytearray(data)
    for span in spans:
        masked[span.start : span.end] = b" " * (span.end - span.start)
    if re.search(rb"(?<!\\)\$", bytes(masked)):
        raise ScanError("unterminated or ambiguous math delimiter")

    spans.sort(key=lambda item: (item.start, item.end))
    for left, right in zip(spans, spans[1:], strict=False):
        if left.end > right.start:
            raise ScanError("overlapping protected constructs")

    # The ledger deliberately ignores only recognized line-format prefixes and
    # whitespace. Every other UTF-8 byte contributes in order.
    content = _LINE_MARKER.sub(b"", data)
    ledger = tuple(sha256(token).hexdigest() for token in re.findall(rb"\S+", content))
    return ScannedDocument(data=data, protected=tuple(spans), ledger=ledger)
