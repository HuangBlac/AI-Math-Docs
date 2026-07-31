from pathlib import Path

from typer.testing import CliRunner

from ai_math_study.cli import app


runner = CliRunner()


def _project(tmp_path: Path) -> Path:
    study = tmp_path / ".study"
    generation = "gen-" + "b" * 64
    (study / "generations" / generation).mkdir(parents=True)
    (study / "CURRENT").write_text(generation + "\n", encoding="ascii")
    pdf = tmp_path / "lftp.pdf"
    pdf.write_bytes(b"locked")
    import hashlib

    digest = hashlib.sha256(b"locked").hexdigest()
    config = tmp_path / "study.toml"
    config.write_text(
        "\n".join(
            [
                "[project]",
                'root = "."',
                'study_dir = ".study"',
                'pdf = "lftp.pdf"',
                f'expected_pdf_sha256 = "{digest}"',
                "chapters = [1,2,3,4,5,6,7,8,9]",
                "[sources]",
                "markdown_roots = []",
                "[models]",
                'generator = "x"',
                'grader = "x"',
                'note_worker = "x"',
                'critic = "x"',
                "[subagents]",
                "max_concurrency = 1",
                "[mastery]",
                "pass_score = 80",
            ]
        ),
        encoding="utf-8",
    )
    return config


def test_cli_inventory_and_unicode_output(tmp_path: Path) -> None:
    config = _project(tmp_path)
    result = runner.invoke(app, ["exercise", "inventory", "--chapter", "8", "--config", str(config)])
    assert result.exit_code == 0
    assert "第 8 章" in result.stdout
    assert "17" in result.stdout


def test_cli_attempt_status_weekly_and_doctor(tmp_path: Path) -> None:
    config = _project(tmp_path)
    answer = tmp_path / "答案.md"
    answer.write_text("证明内容", encoding="utf-8")
    attempted = runner.invoke(
        app, ["exercise", "attempt", "9.1", str(answer), "--config", str(config)]
    )
    assert attempted.exit_code == 0
    assert "已记录" in attempted.stdout
    status = runner.invoke(app, ["exercise", "status", "9.1", "--config", str(config)])
    assert status.exit_code == 0
    assert "submitted" in status.stdout
    weekly = runner.invoke(app, ["weekly", "--config", str(config)])
    assert weekly.exit_code == 0
    assert "本周进度" in weekly.stdout
    doctor = runner.invoke(app, ["state", "doctor", "--config", str(config)])
    assert doctor.exit_code == 0
    assert "状态账本健康" in doctor.stdout

