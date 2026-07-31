from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ai_math_study.config import StudyConfig
from ai_math_study.ingest.generation import resolve_current_generation
from ai_math_study.state import LearningProgressService, StateStore


console = Console(highlight=False)
state_app = typer.Typer(help="检查本地学习状态账本", no_args_is_help=True)
exercise_app = typer.Typer(help="查看习题清单并记录作答", no_args_is_help=True)
ConfigOption = Annotated[Path, typer.Option("--config", help="study.toml 路径")]


def _config(path: Path) -> StudyConfig:
    return StudyConfig.load(path)


def _progress(config: StudyConfig) -> LearningProgressService:
    generation = resolve_current_generation(config.study_dir).name
    return LearningProgressService(StateStore(config.study_dir / "state.sqlite3"), generation)


@state_app.command("doctor")
def state_doctor(config: ConfigOption = Path("study.toml")) -> None:
    try:
        report = _progress(_config(config)).store.doctor()
    except (OSError, ValueError) as exc:
        console.print(f"[red]状态账本检查失败：{exc}[/red]")
        raise typer.Exit(1) from exc
    if not report.ok:
        for issue in report.issues:
            console.print(f"[red]- {issue}[/red]")
        raise typer.Exit(1)
    console.print(
        f"[green]状态账本健康[/green] events={report.event_count}, "
        f"pinned_generations={report.pinned_generation_count}"
    )


@exercise_app.command("inventory")
def exercise_inventory(
    chapter: Annotated[int | None, typer.Option(min=1, max=9)] = None,
    config: ConfigOption = Path("study.toml"),
) -> None:
    inventory = _progress(_config(config)).exercise_inventory(chapter)
    scope = f"第 {chapter} 章" if chapter else "前九章"
    console.print(f"[green]{scope} Exercise 清单[/green]：{inventory.total} 题")
    console.print(
        f"无菱形={inventory.unmarked}, 带菱形={inventory.diamond_marked}; "
        "Exercise 1.14 已按锁定 PDF 原页确认带单菱形，其余题目按章签认"
    )
    console.print(" ".join(item.rsplit(":", 1)[-1] for item in inventory.exercise_ids))


@exercise_app.command("status")
def exercise_status(
    exercise: Annotated[str, typer.Argument(help="习题编号，如 9.1")],
    status: Annotated[str | None, typer.Option(help="可选：设置新状态")] = None,
    config: ConfigOption = Path("study.toml"),
) -> None:
    service = _progress(_config(config))
    try:
        overlay = service.set_exercise_status(exercise, status) if status else service.exercise_status(exercise)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print(
        f"{exercise}: status={overlay.status}, attempts={overlay.attempt_count}, version={overlay.version}"
    )


@exercise_app.command("attempt")
def exercise_attempt(
    exercise: Annotated[str, typer.Argument(help="习题编号，如 9.1")],
    answer: Annotated[Path, typer.Argument(exists=True, dir_okay=False, help="UTF-8 答案文件")],
    config: ConfigOption = Path("study.toml"),
) -> None:
    try:
        overlay = _progress(_config(config)).record_exercise_attempt(exercise, answer)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    console.print(
        f"[green]已记录[/green] Exercise {exercise}; attempts={overlay.attempt_count}; "
        "账本仅保存答案哈希"
    )


def weekly_progress(config: ConfigOption = Path("study.toml")) -> None:
    summary = _progress(_config(config)).weekly_summary()
    console.print("[green]本周进度[/green]")
    console.print(
        f"Exercise: 总计={summary.total}, 尝试={summary.attempts}, "
        f"已闭环={summary.closed}, 待闭环={summary.remaining}"
    )


def start(config: ConfigOption = Path("study.toml")) -> None:
    cfg = _config(config)
    console.print("[bold]LFTP 学习工作台[/bold]")
    try:
        generation = resolve_current_generation(cfg.study_dir).name
        console.print(f"当前教材语料：{generation[:20]}…")
    except (OSError, ValueError) as exc:
        console.print(f"[yellow]语料库尚未就绪：{exc}[/yellow]")
    console.print("常用操作：state doctor | exercise inventory | exercise attempt | weekly")


def register_progress_commands(app: typer.Typer) -> None:
    app.add_typer(state_app, name="state")
    app.add_typer(exercise_app, name="exercise")
    app.command("weekly")(weekly_progress)
    app.command("start")(start)
