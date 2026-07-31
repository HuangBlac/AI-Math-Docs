from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import sys
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ai_math_study.config import StudyConfig
from ai_math_study.domain.problems import ProblemType
from ai_math_study.domain.syllabus import load_default_syllabus
from ai_math_study.generator import ProblemGenerator
from ai_math_study.grader import EvidenceGrader
from ai_math_study.guide import build_chapter_skeleton, build_study_plan
from ai_math_study.ingest import IngestConfig, build_corpus, doctor_corpus
from ai_math_study.ingest.generation import resolve_corpus_database
from ai_math_study.notes import NoteOrganizer
from ai_math_study.notes.formatter import FormatError, FormatOperation, paste_preview
from ai_math_study.notes.publisher import PublishError, publish_new
from ai_math_study.ports.llm import ProviderProfile
from ai_math_study.providers import DeepSeekProvider, DryRunProvider, FakeProvider, OpenAIProvider, ReplayProvider
from ai_math_study.progress_cli import register_progress_commands
from ai_math_study.retrieval import build_evidence_packet, search_corpus
from ai_math_study.serde import load_problem_bundle, write_json


console = Console(highlight=False)
app = typer.Typer(help="LFTP 前九章可验证学习工作台", no_args_is_help=True)
ingest_app = typer.Typer(help="构建和检查本地教材/笔记语料库", no_args_is_help=True)
guide_app = typer.Typer(help="生成仅存本地的中文精读工作包", no_args_is_help=True)
corpus_app = typer.Typer(help="检索带出处的知识原子", no_args_is_help=True)
notes_app = typer.Typer(help="多 agent Markdown/LaTeX 笔记整理", no_args_is_help=True)
app.add_typer(ingest_app, name="ingest")
app.add_typer(guide_app, name="guide")
app.add_typer(corpus_app, name="corpus")
app.add_typer(notes_app, name="notes")
register_progress_commands(app)


ConfigOption = Annotated[Path, typer.Option("--config", help="study.toml 路径")]


def _config(path: Path) -> StudyConfig:
    return StudyConfig.load(path)


def _parse_chapters(value: str) -> tuple[int, ...]:
    chapters: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = (int(item) for item in part.split("-", 1))
            chapters.update(range(start, end + 1))
        else:
            chapters.add(int(part))
    if not chapters or not chapters.issubset(set(range(1, 10))):
        raise typer.BadParameter("chapters must be a subset of 1-9")
    return tuple(sorted(chapters))


def _load_provider(
    name: str,
    fixture: Path | None = None,
    *,
    profile: ProviderProfile | None = None,
):
    normalized = name.casefold()
    if normalized == "openai":
        if profile is not None and profile.provider != "openai":
            raise typer.BadParameter("the selected role has no OpenAI model profile")
        return OpenAIProvider()
    if normalized == "deepseek":
        if profile is None or profile.provider != "deepseek":
            raise typer.BadParameter("a DeepSeek model profile is required for this role")
        return DeepSeekProvider(profile)
    if normalized in {"fake", "replay", "dry-run"} and fixture is None:
        raise typer.BadParameter(f"--fixture is required for provider {normalized}")
    payload = json.loads(fixture.read_text(encoding="utf-8")) if fixture else None
    if normalized == "fake":
        responses = payload if isinstance(payload, list) else [payload]
        return FakeProvider(responses)
    if normalized == "replay":
        if not isinstance(payload, dict):
            raise typer.BadParameter("replay fixture must be an object keyed by request hash")
        return ReplayProvider(payload)
    if normalized == "dry-run":
        if not isinstance(payload, dict):
            raise typer.BadParameter("dry-run preview fixture must be an object")
        return DryRunProvider(payload)
    raise typer.BadParameter("provider must be openai, deepseek, fake, replay, or dry-run")


@ingest_app.command("build")
def ingest_build(
    chapters: Annotated[str, typer.Option(help="章节，如 1-9 或 3,5,6")] = "1-9",
    config: ConfigOption = Path("study.toml"),
) -> None:
    cfg = _config(config)
    cfg.verify_pdf()
    selected = _parse_chapters(chapters)
    result = build_corpus(
        IngestConfig(
            project_root=cfg.root,
            pdf_path=cfg.pdf,
            manifest=load_default_syllabus(),
            markdown_roots=cfg.markdown_roots,
            study_dir=cfg.study_dir,
            chapters=selected,
        )
    )
    console.print(
        f"[green]语料库已构建[/green] sources={result.source_count}, atoms={result.atom_count}, "
        f"reviews={result.review_count}, manifest={result.manifest_sha256[:16]}"
    )


@ingest_app.command("doctor")
def ingest_doctor(config: ConfigOption = Path("study.toml")) -> None:
    cfg = _config(config)
    issues: list[str] = []
    try:
        cfg.verify_pdf()
    except (OSError, ValueError) as exc:
        issues.append(str(exc))
    report = doctor_corpus(cfg.study_dir)
    issues.extend(report.issues)
    if issues:
        for issue in issues:
            console.print(f"[red]- {issue}[/red]")
        raise typer.Exit(1)
    console.print(
        f"[green]健康[/green] sources={report.source_count}, atoms={report.atom_count}, "
        f"reviews={report.review_count}; OPENAI_API_KEY={'set' if os.getenv('OPENAI_API_KEY') else 'not set'}"
    )


@guide_app.command("build")
def guide_build(
    chapter: Annotated[int | None, typer.Option(min=1, max=9, help="省略时生成全部九章")] = None,
    config: ConfigOption = Path("study.toml"),
) -> None:
    cfg = _config(config)
    plan = build_study_plan(cfg.study_dir)
    chapters = [chapter] if chapter else list(cfg.chapters)
    outputs = [build_chapter_skeleton(cfg.study_dir, number) for number in chapters]
    console.print(f"[green]学习计划[/green] {plan}")
    for output in outputs:
        console.print(
            f"[green]精读包[/green] Ch{output.chapter}: {output.guide_path}; "
            f"Exercise={output.exercise_path}; 公式队列={output.formula_queue_path}"
        )


@corpus_app.command("search")
def corpus_search(
    query: Annotated[str, typer.Argument(help="中文或英文检索词")],
    chapter: Annotated[int | None, typer.Option(min=1, max=9)] = None,
    limit: Annotated[int, typer.Option(min=1, max=100)] = 10,
    config: ConfigOption = Path("study.toml"),
) -> None:
    cfg = _config(config)
    hits = search_corpus(resolve_corpus_database(cfg.study_dir), query, limit, chapter=chapter)
    table = Table("claim_id", "章/节", "类型", "核验", "出处", "内容")
    for hit in hits:
        location = hit.locator.get("path", "")
        table.add_row(
            hit.claim_id,
            f"{hit.chapter or '-'} / {hit.section or '-'}",
            hit.knowledge_type,
            hit.verification_state,
            str(location),
            hit.statement_zh[:100],
        )
    console.print(table)


@app.command("generate")
def generate_problem(
    query: Annotated[str, typer.Option(help="用于冻结证据包的检索词")],
    problem_type: Annotated[ProblemType, typer.Option("--type")] = ProblemType.PROOF,
    chapter: Annotated[int | None, typer.Option(min=1, max=9)] = None,
    count: Annotated[int, typer.Option(min=1, max=20)] = 1,
    provider: Annotated[str, typer.Option()] = "deepseek",
    fixture: Annotated[Path | None, typer.Option(exists=True, dir_okay=False)] = None,
    output_dir: Annotated[Path | None, typer.Option()] = None,
    config: ConfigOption = Path("study.toml"),
) -> None:
    cfg = _config(config)
    database_path = resolve_corpus_database(cfg.study_dir)
    hits = search_corpus(database_path, query, 20, chapter=chapter)
    if not hits:
        raise typer.BadParameter("检索没有命中，无法冻结证据包")
    packet = build_evidence_packet(database_path, hits, limit=12)
    role = {
        ProblemType.PROOF: "proof_generator",
        ProblemType.COUNTEREXAMPLE: "counterexample_generator",
    }.get(problem_type, "generator")
    profile = cfg.model_profiles[role]
    generator = ProblemGenerator(
        _load_provider(provider, fixture, profile=profile),
        model=profile.model,
    )
    target_dir = output_dir or cfg.study_dir / "questions"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for index in range(1, count + 1):
        problem = generator.generate(problem_type, packet)
        target = target_dir / f"{stamp}-{problem_type.value}-{index:02d}.json"
        write_json(target, {"problem": problem, "evidence": packet})
        console.print(f"[green]题目已生成[/green] {target}")


@app.command("grade")
def grade_answer(
    problem_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    answer_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    provider: Annotated[str, typer.Option()] = "deepseek",
    fixture: Annotated[Path | None, typer.Option(exists=True, dir_okay=False)] = None,
    output: Annotated[Path | None, typer.Option()] = None,
    config: ConfigOption = Path("study.toml"),
) -> None:
    cfg = _config(config)
    problem, packet = load_problem_bundle(problem_file, study_dir=cfg.study_dir)
    answer = answer_file.read_text(encoding="utf-8")
    profile = cfg.model_profiles["grader"]
    report = EvidenceGrader(
        _load_provider(provider, fixture, profile=profile), model=profile.model
    ).grade(
        problem, answer, packet
    )
    target = output or cfg.study_dir / "grades" / f"{problem.problem_id}.json"
    write_json(target, report)
    status = "[yellow]人工复核[/yellow]" if report.manual_review else "[green]已核验[/green]"
    console.print(f"{status} score={report.score}/{report.max_score} ({report.percentage}%) -> {target}")
    console.print("AI 辅助判分，不等同于 Lean/Coq 形式化验证。")


@notes_app.command("tidy")
def notes_tidy(
    source: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    apply: Annotated[bool, typer.Option(help="通过全部校验后原子替换源文件")] = False,
    patch_file: Annotated[Path | None, typer.Option("--patch", help="保存统一 diff") ] = None,
    repair_math: Annotated[bool, typer.Option(help="另行生成公式修复建议，绝不自动应用")] = False,
    provider: Annotated[str, typer.Option()] = "deepseek",
    fixture: Annotated[Path | None, typer.Option(exists=True, dir_okay=False)] = None,
    config: ConfigOption = Path("study.toml"),
) -> None:
    cfg = _config(config)
    if apply:
        raise typer.BadParameter("V1 organize 只生成 proposal，禁止写回源文件；请人工审阅 diff")
    worker_profile = cfg.model_profiles["note_worker"]
    planner_profile = cfg.model_profiles["note_planner"]
    critic_profile = cfg.model_profiles["critic"]
    worker_provider = _load_provider(provider, fixture, profile=worker_profile)
    if provider.casefold() == "deepseek":
        planner_provider = _load_provider(provider, fixture, profile=planner_profile)
        critic_provider = _load_provider(provider, fixture, profile=critic_profile)
    else:
        planner_provider = worker_provider
        critic_provider = worker_provider
    organizer = NoteOrganizer(
        worker_provider,
        model=worker_profile.model,
        planner_provider=planner_provider,
        planner_model=planner_profile.model,
        critic_provider=critic_provider,
        critic_model=critic_profile.model,
        max_concurrency=int(cfg.subagents["max_concurrency"]),
    )
    proposal = organizer.organize_path(source, apply=False)
    proposal_path = cfg.study_dir / "proposals" / f"{source.stem}-{proposal.source_sha256[:12]}.json"
    write_json(proposal_path, proposal)
    if patch_file:
        patch_file.parent.mkdir(parents=True, exist_ok=True)
        patch_file.write_text(proposal.unified_diff, encoding="utf-8")
    if repair_math:
        suggestions = organizer.suggest_math_repairs(source.read_text(encoding="utf-8-sig"))
        repair_path = cfg.study_dir / "review-queue" / f"{source.stem}-math-repairs.json"
        write_json(repair_path, suggestions)
        console.print(f"[yellow]公式建议需人工复核[/yellow] {repair_path}")
    console.print(f"[cyan]仅生成 proposal，源文件未修改[/cyan] proposal={proposal_path}")
    if not proposal.eligible_to_apply:
        console.print("[yellow]当前 proposal 未通过 critic 或确定性校验，不能 apply。[/yellow]")


def _clipboard_bytes() -> bytes:
    try:
        import tkinter

        root = tkinter.Tk()
        root.withdraw()
        try:
            value = root.clipboard_get()
        finally:
            root.destroy()
    except Exception as exc:
        raise typer.BadParameter(f"无法读取剪贴板：{exc}") from exc
    return str(value).encode("utf-8")


def _format_input(source: Path | None, clipboard: bool) -> bytes:
    if source is not None and clipboard:
        raise typer.BadParameter("source 与 --clipboard 只能选择一个")
    if source is not None:
        return source.read_bytes()
    if clipboard:
        return _clipboard_bytes()
    if sys.stdin.isatty():
        raise typer.BadParameter("请提供源文件、--clipboard，或通过标准输入粘贴内容")
    return sys.stdin.buffer.read()


def _heading_operation(value: str) -> FormatOperation:
    try:
        line_text, level_text = value.split(":", 1)
        return FormatOperation.heading(line=int(line_text), level=int(level_text))
    except (TypeError, ValueError) as exc:
        raise typer.BadParameter("--heading 格式必须是 行号:层级，例如 3:2") from exc


@notes_app.command("format")
def notes_format(
    source: Annotated[Path | None, typer.Argument(exists=True, dir_okay=False)] = None,
    output: Annotated[Path | None, typer.Option("--output", "-o", help="只允许不存在的新文件")] = None,
    clipboard: Annotated[bool, typer.Option(help="从系统剪贴板读取 UTF-8 文本")] = False,
    heading: Annotated[list[str] | None, typer.Option("--heading", help="重复使用；格式 行号:层级")] = None,
    list_line: Annotated[list[int] | None, typer.Option("--list-line", help="为指定行添加列表标记")] = None,
) -> None:
    """严格内容守恒的 Markdown 格式修复；默认只预览，绝不覆盖源文件。"""

    data = _format_input(source, clipboard)
    operations = tuple(_heading_operation(value) for value in (heading or ())) + tuple(
        FormatOperation.list_item(line=line) for line in (list_line or ())
    )
    try:
        result = paste_preview(data, operations)
        if output is not None:
            publish_new(output, result)
            console.print(f"[green]已发布新文件[/green] {output}")
        else:
            console.print(result.decode("utf-8"), markup=False, end="")
    except (FormatError, PublishError, UnicodeDecodeError) as exc:
        console.print(f"[red]格式修复被拒绝：{exc}[/red]")
        raise typer.Exit(1) from exc
