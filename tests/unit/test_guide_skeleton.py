from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_math_study.guide.service import build_chapter_skeleton, build_study_plan
from ai_math_study.ingest.generation import generation_id


def _study_dir(tmp_path: Path) -> tuple[Path, str]:
    generation = generation_id({"fixture": "guide-skeleton"})
    generation_dir = tmp_path / "generations" / generation
    generation_dir.mkdir(parents=True)
    (generation_dir / "manifest.json").write_text("{}", encoding="utf-8")
    (tmp_path / "CURRENT").write_text(generation + "\n", encoding="ascii")
    return tmp_path, generation


def test_chapter_skeleton_is_offline_complete_and_generation_bound(tmp_path: Path) -> None:
    study_dir, generation = _study_dir(tmp_path)

    bundle = build_chapter_skeleton(study_dir, 8)

    assert bundle.generation_id == generation
    assert bundle.guide_path == study_dir / "derived" / "lftp" / "ch08" / "guide.md"
    guide = bundle.guide_path.read_text(encoding="utf-8")
    assert "Ch8 Sparse Methods" in guide
    assert "印刷页 221–246 / PDF 页 237–262" in guide
    assert "8.3.6" in guide
    assert "## 定义・假设・量词・结论（待填写）" in guide
    assert "Exercises 8.1-8.17" in guide
    assert "逐页翻译" not in guide

    queue = json.loads(bundle.formula_queue_path.read_text(encoding="utf-8"))
    assert queue["corpus_generation"] == generation
    assert queue["source_sha256"].endswith("E486DEA")
    assert queue["verification_status"] == "unverified"
    assert queue["items"]
    assert all(item["verification_status"] == "unverified" for item in queue["items"])
    assert all(
        {"section", "printed_page", "pdf_page"} <= set(item["anchor"])
        for item in queue["items"]
    )

    manifest = json.loads(bundle.manifest_path.read_text(encoding="utf-8"))
    assert manifest["corpus_generation"] == generation
    assert manifest["source_sha256"].endswith("E486DEA")
    assert manifest["verification_status"] == "unverified"
    assert set(manifest["artifacts"]) == {"guide.md", "formula-verification.json", "exercises.json"}
    assert all(len(item["sha256"]) == 64 for item in manifest["artifacts"].values())


def test_exercise_navigation_preserves_each_diamond_status(tmp_path: Path) -> None:
    study_dir, _ = _study_dir(tmp_path)

    bundle = build_chapter_skeleton(study_dir, 7)
    exercises = json.loads(bundle.exercise_path.read_text(encoding="utf-8"))

    assert len(exercises["items"]) == 23
    assert exercises["items"][0]["exercise"] == "7.1"
    assert exercises["items"][0]["diamond_count"] == 2
    assert exercises["items"][4]["diamond_count"] == 3
    assert all(item["verification_status"] in {"provisional", "source-aligned"} for item in exercises["items"])


def test_strict_skeleton_refuses_an_unbound_corpus(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="CURRENT"):
        build_chapter_skeleton(tmp_path, 1)


def test_study_plan_is_eight_dated_weeks_through_deadline(tmp_path: Path) -> None:
    legacy = tmp_path / "plan" / "14-week-plan.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("stale", encoding="utf-8")
    plan = build_study_plan(tmp_path)

    assert plan.name == "2026-07-12-to-2026-09-05.md"
    text = plan.read_text(encoding="utf-8")
    assert "8 周" in text
    assert "2026-07-12" in text
    assert "2026-09-05" in text
    assert "Ch8 稀疏方法" in text
    assert "Ch9 神经网络" in text
    assert "21 周" not in text
    assert "14-week" not in str(plan)
    assert not legacy.exists()
