from __future__ import annotations

import os
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

from ai_math_study.notes.formatter import (
    FormatError,
    FormatOperation,
    format_utf8,
    paste_preview,
)
from ai_math_study.notes.publisher import PublishError, publish_new
from ai_math_study.notes.scanner import ScanError, scan_utf8


SAMPLE = (
    b"---\ntitle: T\n---\n\n"
    b"Intro\n\n"
    b"`x = 1` and [[Target|label]] and https://example.test/a?q=1\n\n"
    b"$$\\sum_i x_i$$\n\n"
    b"```python\nprint('x')\n```\n"
)


def test_zero_operations_are_byte_exact() -> None:
    assert format_utf8(SAMPLE, ()) == SAMPLE
    assert paste_preview(SAMPLE) == SAMPLE


def test_scanner_protects_frontmatter_code_wikilink_math_and_url() -> None:
    kinds = {span.kind for span in scan_utf8(SAMPLE).protected}
    assert {"frontmatter", "inline_code", "wikilink", "url", "math", "code_fence"} <= kinds


def test_heading_and_list_prefixes_preserve_content_ledger() -> None:
    source = "标题\n条目\n".encode()
    result = format_utf8(
        source,
        (
            FormatOperation.heading(line=1, level=2),
            FormatOperation.list_item(line=2),
        ),
    )
    assert result == "## 标题\n- 条目\n".encode()
    assert scan_utf8(source).ledger == scan_utf8(result).ledger


def test_explicit_whitespace_span_can_be_normalized() -> None:
    source = b"alpha\n\n\n\nbeta\n"
    result = format_utf8(
        source,
        (FormatOperation.replace_whitespace(start=5, end=9, replacement=b"\n\n"),),
    )
    assert result == b"alpha\n\nbeta\n"


def test_non_whitespace_replacement_fails_closed() -> None:
    with pytest.raises(FormatError, match="whitespace bytes only"):
        format_utf8(
            b"a\n\nb",
            (FormatOperation.replace_whitespace(start=1, end=3, replacement=b" title "),),
        )


def test_whitespace_cannot_be_inserted_inside_formula_or_code() -> None:
    for source, offset in ((b"$x+y$\n", 3), (b"`x y`\n", 3)):
        with pytest.raises(FormatError, match="protected"):
            format_utf8(
                source,
                (FormatOperation.replace_whitespace(start=offset, end=offset, replacement=b" "),),
            )


@given(st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=100))
def test_zero_operation_property(text: str) -> None:
    data = text.encode("utf-8")
    assert format_utf8(data, ()) == data


def test_protected_lines_cannot_be_formatted() -> None:
    with pytest.raises(FormatError, match="protected"):
        format_utf8(SAMPLE, (FormatOperation.heading(line=1, level=1),))
    with pytest.raises(FormatError, match="protected"):
        format_utf8(SAMPLE, (FormatOperation.list_item(line=11),))


def test_invalid_utf8_and_ambiguous_markdown_fail_closed() -> None:
    with pytest.raises(ScanError, match="UTF-8"):
        scan_utf8(b"\xff")
    with pytest.raises(ScanError, match="unterminated"):
        scan_utf8(b"```python\nx = 1\n")
    with pytest.raises(ScanError, match="unterminated"):
        scan_utf8(b"text $x\n")


def test_publisher_never_overwrites_and_cleans_partial(tmp_path: Path) -> None:
    target = tmp_path / "note.md"
    publish_new(target, "中文\n".encode())
    assert target.read_bytes() == "中文\n".encode()
    with pytest.raises(PublishError, match="exists"):
        publish_new(target, b"replacement")
    assert target.read_bytes() == "中文\n".encode()
    assert not target.with_name("note.md.partial").exists()


def test_publisher_fails_when_no_replace_is_unavailable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "note.md"
    monkeypatch.setattr(os, "link", lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("no")))
    with pytest.raises(PublishError, match="no-replace"):
        publish_new(target, b"data")
    assert not target.exists()
    assert not target.with_name("note.md.partial").exists()
