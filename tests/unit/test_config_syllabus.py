from __future__ import annotations

import json
from pathlib import Path

from ai_math_study.config import StudyConfig
from ai_math_study.domain.syllabus import load_default_syllabus
from ai_math_study.guide.service import build_guide, build_study_plan


ROOT = Path(__file__).resolve().parents[2]


def test_config_locks_local_pdf() -> None:
    config = StudyConfig.load(ROOT / "study.toml")
    assert config.verify_pdf() == config.expected_pdf_sha256
    assert config.chapters == (1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert config.models["guide"] == "deepseek-v4-flash"
    assert config.model_profiles["guide"].thinking is False
    assert config.model_profiles["grader"].model == "deepseek-v4-pro"
    assert config.model_profiles["grader"].thinking is True
    assert config.openai == {}
    assert config.deepseek["store"] is False


def test_syllabus_has_correct_nine_chapters() -> None:
    syllabus = load_default_syllabus()
    assert syllabus.page_count == 488
    assert [chapter.title_en for chapter in syllabus.chapters] == [
        "Mathematical Preliminaries",
        "Introduction to Supervised Learning",
        "Linear Least-Squares Regression",
        "Empirical Risk Minimization",
        "Optimization for Machine Learning",
        "Local Averaging Methods",
        "Kernel Methods",
        "Sparse Methods",
        "Neural Networks",
    ]
    assert [chapter.pdf_pages for chapter in syllabus.chapters] == [
        [19, 36], [37, 59], [61, 84], [87, 123], [125, 169], [171, 194],
        [195, 236], [237, 262], [263, 296],
    ]
    assert len(syllabus.weeks) == 8
    assert [chapter.chapter for chapter in syllabus.chapters if chapter.priority == "gap_first"] == [3, 5, 6, 7, 8, 9]


def test_locked_pdf_chapters_seven_to_nine_match_truth_manifest() -> None:
    syllabus = load_default_syllabus()
    sections = {
        chapter.chapter: {section.section: section.title_en for section in chapter.sections}
        for chapter in syllabus.chapters
        if chapter.chapter in {7, 8, 9}
    }
    assert sections[7]["7.4.1"] == "Representer Theorem"
    assert sections[7]["7.4.4"] == "Dual Algorithms"
    assert sections[7]["7.4.5"] == "Stochastic Gradient Descent"
    assert sections[7]["7.4.6"] == "Kernelization of Linear Algorithms"
    assert sections[7]["7.6.1"] == "Kernel Ridge Regression as a Linear Estimator"
    assert sections[7]["7.6.4"] == "Analysis for Well-Specified Problems"
    assert sections[7]["7.6.5"] == "Analysis beyond Well-Specified Problems"
    assert sections[7]["7.6.6"] == "Balancing Bias and Variance"
    assert sections[9]["9.3.6"] == "From the Variation Norm to a Finite Number of Neurons"


def test_exercise_inventory_is_metadata_only_and_records_visual_boundary_resolution() -> None:
    fixture_path = ROOT / "tests" / "fixtures" / "lftp_exercises_v1.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert fixture["source_sha256"] == "DDEBA8166E4DC2AEDC0B863E67AF9891178A5E13F3316FD672D49CD59E486DEA"
    assert fixture["verification_status"] == "provisional"
    assert len(fixture["exercises"]) == 154
    assert len({item["exercise_id"] for item in fixture["exercises"]}) == 154
    statuses = {item["number"]: item["verification_status"] for item in fixture["exercises"] if item["chapter"] == 1}
    assert statuses[14] == "source-aligned"
    assert all(
        item["verification_status"] == "provisional"
        for item in fixture["exercises"]
        if not (item["chapter"] == 1 and item["number"] == 14)
    )
    assert all("excerpt" not in item and "text" not in item and "title" not in item for item in fixture["exercises"])

    summary = fixture["summary"]
    assert summary["parser_observed"] == {"total": 154, "unmarked": 96, "diamond_marked": 58}
    assert summary["current_target"] == {"total": 154, "unmarked": 96, "diamond_marked": 58}
    assert summary["historical_planned_target"] == {
        "total": 154,
        "unmarked": 97,
        "diamond_marked": 57,
    }
    assert summary["discrepancy_status"] == "resolved_against_locked_pdf"
    assert fixture["manual_review"]["candidate_exercise_ids"] == [
        "lftp:DDEBA8166E4DC2AEDC0B863E67AF9891178A5E13F3316FD672D49CD59E486DEA:exercise:1.14"
    ]
    assert fixture["manual_review"]["evidence_anchors"][0]["visual_review_status"] == "source_aligned"
    assert fixture["manual_review"]["signed_off_by"] is None
    assert fixture["manual_review"]["signed_off_manifest_sha256"] is None


def test_chapter_seven_to_nine_guide_ranges_do_not_invent_items() -> None:
    blueprints = json.loads(
        (ROOT / "src" / "ai_math_study" / "data" / "guide_blueprints.json").read_text(encoding="utf-8")
    )
    assert blueprints["7"]["exercise_focus"] == ["Prop. 7.1-7.8", "Exercises 7.1-7.23"]
    assert blueprints["8"]["exercise_focus"] == ["Prop. 8.1-8.6", "Exercises 8.1-8.17"]
    assert blueprints["9"]["exercise_focus"] == ["Prop. 9.1-9.3", "Exercises 9.1-9.10"]


def test_private_guides_render_to_requested_directory(tmp_path: Path) -> None:
    guide = build_guide(tmp_path, 3)
    plan = build_study_plan(tmp_path)
    assert guide.is_file() and plan.is_file()
    guide_text = guide.read_text(encoding="utf-8")
    assert "线性最小二乘回归" in guide_text
    assert "PDF 页 61–84" in guide_text
    assert "逐页" not in guide_text
    assert "8 周" in plan.read_text(encoding="utf-8")
