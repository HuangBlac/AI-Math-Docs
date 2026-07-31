from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ai_math_study.notes import (  # noqa: E402
    NoteApplyError,
    NoteOrganizer,
    apply_note_proposal,
)


class FakeNoteProvider:
    def __init__(self, *, worker_mode: str = "normal", critic_approved: bool = True) -> None:
        self.worker_mode = worker_mode
        self.critic_approved = critic_approved
        self.calls: list[str] = []
        self.requests: list[object] = []
        self._lock = threading.Lock()
        self._active_workers = 0
        self.max_active_workers = 0

    def generate(self, request: object) -> dict:
        schema_name = getattr(request, "schema_name")
        payload = json.loads(getattr(request, "input_text"))
        with self._lock:
            self.calls.append(schema_name)
            self.requests.append(request)

        if schema_name == "note_plan_v1":
            sections = []
            for index, fragment in enumerate(payload["fragments"], 1):
                sections.append(
                    {
                        "section_id": f"section-{index}",
                        "heading": fragment.get("heading_hint") or f"整理部分 {index}",
                        "source_fragment_ids": [fragment["fragment_id"]],
                        "instructions": "保留原意，改善段落顺序。",
                    }
                )
            return {"document_title": payload.get("existing_title") or "整理后的笔记", "sections": sections}

        if schema_name == "note_section_v1":
            with self._lock:
                self._active_workers += 1
                self.max_active_workers = max(self.max_active_workers, self._active_workers)
            try:
                time.sleep(0.05)
                body = "\n\n".join(item["markdown"] for item in payload["fragments"])
                tokens = payload["required_tokens"]
                if self.worker_mode == "drop" and tokens:
                    body = body.replace(tokens[0], "", 1)
                elif self.worker_mode == "duplicate" and tokens:
                    body += "\n" + tokens[0]
                elif self.worker_mode == "invent":
                    body += "\n@@AIMATH_INLINE_MATH_9999_deadbeefdead@@"
                return {"section_id": payload["section"]["section_id"], "body_markdown": body}
            finally:
                with self._lock:
                    self._active_workers -= 1

        if schema_name == "note_critique_v1":
            return {
                "approved": self.critic_approved,
                "summary": "结构与保护项检查完成。",
                "issues": [] if self.critic_approved else [
                    {
                        "severity": "error",
                        "code": "critic_rejected",
                        "message": "仍需人工整理。",
                        "section_id": None,
                    }
                ],
            }

        raise AssertionError(f"Unexpected schema: {schema_name}")


class RoleProvider(FakeNoteProvider):
    def __init__(self, role: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.role = role
        self.models: list[str] = []

    def generate(self, request: object) -> dict:
        self.models.append(getattr(request, "model"))
        return super().generate(request)


SOURCE = r"""---
title: 原笔记
---

# 原笔记

## 风险

这里是 [[erm|经验风险]]，定义为 $R(f)=\mathbb E[\ell(Y,f(X))]$。

## 复杂度

```python
print("keep me")
```

并使用公式

$$
\widehat R_n(f)=\frac1n\sum_{i=1}^n \ell(Y_i,f(X_i)).
$$
"""


class NoteOrchestratorTests(unittest.TestCase):
    def test_fixed_dag_runs_workers_in_parallel_and_preserves_math(self) -> None:
        provider = FakeNoteProvider()
        organizer = NoteOrganizer(provider, model="fake-model", max_concurrency=3)

        proposal = organizer.organize_text(SOURCE, source_name="notes.md")

        self.assertEqual(provider.calls[0], "note_plan_v1")
        self.assertEqual(provider.calls[-1], "note_critique_v1")
        self.assertEqual(provider.calls.count("note_section_v1"), 2)
        self.assertGreaterEqual(provider.max_active_workers, 2)
        self.assertFalse(proposal.applied)
        self.assertTrue(proposal.eligible_to_apply)
        self.assertIn(r"$R(f)=\mathbb E[\ell(Y,f(X))]$", proposal.proposed_markdown)
        self.assertIn(r"\widehat R_n(f)=\frac1n\sum_{i=1}^n", proposal.proposed_markdown)
        self.assertEqual(proposal.proposed_markdown.count("# 原笔记"), 1)
        self.assertNotIn("@@AIMATH_", proposal.proposed_markdown)
        self.assertNotIn("note_math_repair", provider.calls)

    def test_default_path_operation_only_returns_patch_preview(self) -> None:
        provider = FakeNoteProvider()
        organizer = NoteOrganizer(provider, model="fake-model")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(SOURCE, encoding="utf-8")

            proposal = organizer.organize_path(path)

            self.assertEqual(path.read_text(encoding="utf-8"), SOURCE)
            self.assertFalse(proposal.applied)
            self.assertIn("--- a/note.md", proposal.unified_diff)
            self.assertIn("+++ b/note.md", proposal.unified_diff)

    def test_apply_api_is_disabled_for_organize_proposals(self) -> None:
        provider = FakeNoteProvider()
        organizer = NoteOrganizer(provider, model="fake-model")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(SOURCE, encoding="utf-8")
            proposal = organizer.organize_path(path)

            with self.assertRaisesRegex(NoteApplyError, "organize.*proposal"):
                apply_note_proposal(path, proposal)
            self.assertEqual(path.read_text(encoding="utf-8"), SOURCE)

    def test_apply_remains_disabled_when_input_changed(self) -> None:
        provider = FakeNoteProvider()
        organizer = NoteOrganizer(provider, model="fake-model")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(SOURCE, encoding="utf-8")
            proposal = organizer.organize_path(path)
            path.write_text(SOURCE + "\n用户同时修改。\n", encoding="utf-8")

            with self.assertRaisesRegex(NoteApplyError, "proposal-only"):
                apply_note_proposal(path, proposal)

    def test_critic_rejection_makes_proposal_ineligible(self) -> None:
        provider = FakeNoteProvider(critic_approved=False)
        organizer = NoteOrganizer(provider, model="fake-model")
        proposal = organizer.organize_text(SOURCE)
        self.assertFalse(proposal.eligible_to_apply)

    def test_routes_planner_workers_and_critic_to_distinct_providers_and_models(self) -> None:
        planner = RoleProvider("planner")
        worker = RoleProvider("worker")
        critic = RoleProvider("critic")
        organizer = NoteOrganizer(
            worker,
            model="worker-model",
            planner_provider=planner,
            planner_model="planner-model",
            critic_provider=critic,
            critic_model="critic-model",
        )

        organizer.organize_text(SOURCE)

        self.assertEqual(planner.calls, ["note_plan_v1"])
        self.assertTrue(worker.calls and set(worker.calls) == {"note_section_v1"})
        self.assertEqual(critic.calls, ["note_critique_v1"])
        self.assertEqual(planner.models, ["planner-model"])
        self.assertTrue(worker.models and set(worker.models) == {"worker-model"})
        self.assertEqual(critic.models, ["critic-model"])

    def test_organize_never_applies_to_source_even_when_requested(self) -> None:
        organizer = NoteOrganizer(FakeNoteProvider(), model="fake-model")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(SOURCE, encoding="utf-8")

            with self.assertRaisesRegex(NoteApplyError, "organize.*proposal"):
                organizer.organize_path(path, apply=True)

            self.assertEqual(path.read_text(encoding="utf-8"), SOURCE)


if __name__ == "__main__":
    unittest.main()
