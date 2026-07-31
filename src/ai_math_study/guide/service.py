from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from importlib.resources import files
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from ai_math_study.domain.syllabus import ChapterSpec, Syllabus, load_default_syllabus
from ai_math_study.ingest.generation import resolve_current_generation


@dataclass(frozen=True)
class ChapterSkeletonBundle:
    chapter: int
    generation_id: str
    guide_path: Path
    exercise_path: Path
    formula_queue_path: Path
    manifest_path: Path


_WEEKS = (
    (1, "2026-07-12", "2026-07-18", "Ch1–2 诊断与压缩学习"),
    (2, "2026-07-19", "2026-07-25", "Ch3 线性最小二乘"),
    (3, "2026-07-26", "2026-08-01", "Ch4 经验风险最小化"),
    (4, "2026-08-02", "2026-08-08", "Ch5 机器学习优化"),
    (5, "2026-08-09", "2026-08-15", "Ch6 局部平均方法"),
    (6, "2026-08-16", "2026-08-22", "Ch7 核方法"),
    (7, "2026-08-23", "2026-08-29", "Ch8 稀疏方法"),
    (8, "2026-08-30", "2026-09-05", "Ch9 神经网络与跨章总结"),
)


def _load_json_resource(name: str) -> Any:
    resource = files("ai_math_study.data").joinpath(name)
    return json.loads(resource.read_text(encoding="utf-8"))


def _load_blueprints() -> dict[str, dict[str, list[str]]]:
    return _load_json_resource("guide_blueprints.json")


def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _anchor_label(chapter: ChapterSpec) -> str:
    return (
        f"印刷页 {chapter.printed_pages[0]}–{chapter.printed_pages[1]} / "
        f"PDF 页 {chapter.pdf_pages[0]}–{chapter.pdf_pages[1]}"
    )


def _chapter_guide(chapter: ChapterSpec, blueprint: dict[str, list[str]], exercises: list[dict[str, Any]]) -> str:
    section_rows = "\n".join(
        f"| {item.section} | {item.title_en} | {item.title_zh} | {item.printed_page} | {item.pdf_page} |"
        for item in chapter.sections
    )
    exercise_rows = "\n".join(
        f"| {item['chapter']}.{item['number']} | {item['diamond_count']} | "
        f"{item['verification_status']} |"
        for item in exercises
    )
    return f"""# Ch{chapter.chapter} {chapter.title_en} / {chapter.title_zh}

> 私人本地精读骨架；仅生成结构化导航和待核验槽位。
> 来源锚点：Ch{chapter.chapter} / {_anchor_label(chapter)}
> 骨架核验状态：`unverified`

## 掌握目标

{_bullet_list(chapter.mastery_objectives)}

## 章节地图（三重锚点）

| 节号 | English | 中文 | 印刷页 | PDF 页 |
|---|---|---|---:|---:|
{section_rows}

## 核心术语

{_bullet_list(blueprint['terms'])}

## 定义・假设・量词・结论（待填写）

| 节号 | 类型 | 中文陈述 | English term | 假设 | 量词 | 结论 | 证据编号 | 状态 |
|---|---|---|---|---|---|---|---|---|
| 待填写 | definition/theorem | | | | | | | unverified |

## 证明依赖链（待核验）

{_bullet_list(blueprint['proof_chain'])}

## 关键例子、边界情形与最小反例

{_bullet_list(blueprint['examples'])}

## Proposition / Exercise 导航

{_bullet_list(blueprint['exercise_focus'])}

| Exercise | 菱形数 | 核验状态 |
|---|---:|---|
{exercise_rows}

## 公式视觉核验队列

详见 `formula-verification.json`。公式只有在人工对照原 PDF 页后才能从
`unverified` 升级为 `verified`。

## 常见误解与自检

{_bullet_list(chapter.misconception_tags)}

## 学习记录

- [ ] 我能闭卷画出概念与证明依赖图
- [ ] 无菱形 Exercise 均有有效作答且通过/已纠正
- [ ] 诊断综合分不低于 80/100，且无致命误解
"""


def _write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def _write_json(path: Path, value: Any) -> None:
    _write_atomic(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def _file_record(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {"sha256": sha256(payload).hexdigest(), "bytes": len(payload)}


def _chapter(syllabus: Syllabus, chapter_number: int) -> ChapterSpec:
    chapter = next((item for item in syllabus.chapters if item.chapter == chapter_number), None)
    if chapter is None:
        raise ValueError(f"Chapter {chapter_number} is not in the syllabus (chapters 1-{len(syllabus.chapters)})")
    return chapter


def build_chapter_skeleton(
    study_dir: Path,
    chapter_number: int,
    syllabus: Syllabus | None = None,
) -> ChapterSkeletonBundle:
    """Build a deterministic, API-free chapter workbench bound to CURRENT."""

    syllabus = syllabus or load_default_syllabus()
    chapter = _chapter(syllabus, chapter_number)
    generation = resolve_current_generation(study_dir)
    generation_name = generation.name
    blueprint = _load_blueprints()[str(chapter_number)]
    inventory = _load_json_resource("lftp_exercises_v1.json")
    exercises = [item for item in inventory["exercises"] if item["chapter"] == chapter_number]
    target = study_dir / "derived" / "lftp" / f"ch{chapter_number:02d}"
    guide_path = target / "guide.md"
    exercise_path = target / "exercises.json"
    formula_path = target / "formula-verification.json"
    manifest_path = target / "manifest.json"

    _write_atomic(guide_path, _chapter_guide(chapter, blueprint, exercises).encode())
    _write_json(
        exercise_path,
        {
            "schema_version": 1,
            "chapter": chapter_number,
            "source_sha256": syllabus.source_sha256,
            "corpus_generation": generation_name,
            "verification_status": "provisional",
            "items": [
                {
                    "exercise_id": item["exercise_id"],
                    "exercise": f"{item['chapter']}.{item['number']}",
                    "diamond_count": item["diamond_count"],
                    "verification_status": item["verification_status"],
                }
                for item in exercises
            ],
        },
    )
    queue_items = []
    for index, check in enumerate(blueprint["formula_checks"], start=1):
        anchor = chapter.sections[min(index - 1, len(chapter.sections) - 1)]
        queue_items.append(
            {
                "formula_id": f"lftp:ch{chapter_number}:formula-check:{index}",
                "check": check,
                "anchor": {
                    "section": anchor.section,
                    "printed_page": anchor.printed_page,
                    "pdf_page": anchor.pdf_page,
                },
                "latex_transcription": None,
                "verification_status": "unverified",
                "verified_by": None,
                "verified_at": None,
            }
        )
    _write_json(
        formula_path,
        {
            "schema_version": 1,
            "chapter": chapter_number,
            "source_sha256": syllabus.source_sha256,
            "corpus_generation": generation_name,
            "verification_status": "unverified",
            "items": queue_items,
        },
    )
    artifacts = {
        path.name: _file_record(path)
        for path in (guide_path, formula_path, exercise_path)
    }
    _write_json(
        manifest_path,
        {
            "schema_version": 1,
            "chapter": chapter_number,
            "source_sha256": syllabus.source_sha256,
            "corpus_generation": generation_name,
            "verification_status": "unverified",
            "artifacts": artifacts,
        },
    )
    return ChapterSkeletonBundle(
        chapter_number, generation_name, guide_path, exercise_path, formula_path, manifest_path
    )


def build_guide(study_dir: Path, chapter_number: int, syllabus: Syllabus | None = None) -> Path:
    """Compatibility service for callers that have not built a corpus yet."""

    syllabus = syllabus or load_default_syllabus()
    chapter = _chapter(syllabus, chapter_number)
    inventory = _load_json_resource("lftp_exercises_v1.json")
    exercises = [item for item in inventory["exercises"] if item["chapter"] == chapter_number]
    target = study_dir / "derived" / "lftp" / f"ch{chapter_number:02d}" / "guide.md"
    _write_atomic(target, _chapter_guide(chapter, _load_blueprints()[str(chapter_number)], exercises).encode())
    return target


def build_study_plan(study_dir: Path, syllabus: Syllabus | None = None) -> Path:
    syllabus = syllabus or load_default_syllabus()
    rows = "\n".join(f"| {week} | {start} | {end} | {focus} | 20h |" for week, start, end, focus in _WEEKS)
    text = f"""# LFTP 前九章 8 周学习计划

> 周期：2026-07-12 至 2026-09-05；每周 20 小时。
> 主教材 SHA-256：`{syllabus.source_sha256}`。

| 周 | 开始 | 结束 | 主线 | 预算 |
|---:|---|---|---|---:|
{rows}

## 不可压缩项

- 前九章非菱形核心正文。
- 96 道无菱形 Exercise 的作答、检查和纠正闭环。
- 核心公式视觉核验、章节诊断和致命误解清零。

## 落后时的压缩顺序

1. 暂停笔记美化。
2. 缩短中文补充解释。
3. 减少单菱形挑战题。
4. 最后才取消额外生成题。
"""
    target = study_dir / "plan" / "2026-07-12-to-2026-09-05.md"
    _write_atomic(target, text.encode())
    for legacy_name in (
        "14-week-plan.md",
        "21-week-plan.md",
        "2026-07-13-to-2026-09-05.md",
    ):
        (target.parent / legacy_name).unlink(missing_ok=True)
    return target
