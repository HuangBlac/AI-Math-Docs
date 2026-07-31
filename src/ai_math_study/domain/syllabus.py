from __future__ import annotations

from importlib.resources import files
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Anchor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    section: str
    title_en: str
    title_zh: str
    printed_page: int
    pdf_page: int
    depth: int


class ChapterSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chapter: int
    title_en: str
    title_zh: str
    printed_pages: list[int]
    pdf_pages: list[int]
    priority: Literal["gap_first", "verify_existing"]
    mastery_objectives: list[str]
    misconception_tags: list[str]
    sections: list[Anchor]


class WeekSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    week: int
    chapters: list[int]
    focus: str
    deliverable: str


class Syllabus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1.0"] = "1.0"
    book_title: str
    source_sha256: str
    page_count: int
    chapters: list[ChapterSpec]
    weeks: list[WeekSpec]
    fatal_misconceptions: list[str]


def load_default_syllabus() -> Syllabus:
    resource = files("ai_math_study.data").joinpath("lftp_syllabus.json")
    payload = json.loads(resource.read_text(encoding="utf-8"))
    schedule = files("ai_math_study.data").joinpath("eight_week_schedule.json")
    payload["weeks"] = json.loads(schedule.read_text(encoding="utf-8"))
    return Syllabus.model_validate(payload)
