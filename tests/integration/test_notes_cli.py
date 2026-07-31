from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ai_math_study.cli import app


runner = CliRunner()


def test_notes_format_reads_stdin_and_publishes_only_a_new_file(tmp_path: Path) -> None:
    output = tmp_path / "formatted.md"
    result = runner.invoke(
        app,
        ["notes", "format", "--heading", "1:1", "--output", str(output)],
        input="Title\nBody\n",
    )

    assert result.exit_code == 0, result.output
    assert output.read_bytes() == b"# Title\nBody\n"

    repeated = runner.invoke(
        app,
        ["notes", "format", "--heading", "1:1", "--output", str(output)],
        input="Title\nBody\n",
    )
    assert repeated.exit_code == 1
    assert output.read_bytes() == b"# Title\nBody\n"


def test_notes_tidy_rejects_apply_before_any_model_call(tmp_path: Path) -> None:
    source = tmp_path / "note.md"
    source.write_text("content\n", encoding="utf-8")

    result = runner.invoke(app, ["notes", "tidy", str(source), "--apply"])

    assert result.exit_code != 0
    assert "禁止写回源文件" in result.output
    assert source.read_text(encoding="utf-8") == "content\n"
