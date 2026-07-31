from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Any, Mapping

from pydantic import ValidationError

from ai_math_study.domain.evidence import EvidenceIntegrityError, EvidencePacket
from ai_math_study.domain.sources import stable_hash
from ai_math_study.domain.problems import (
    GeneratedProblem,
    ProblemType,
    RubricCriterion,
    RubricLevel,
)


def jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return jsonable(value.model_dump(mode="json"))
    if is_dataclass(value):
        return jsonable(asdict(value))  # type: ignore[arg-type]
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [jsonable(item) for item in value]
    return value


def write_json(path: str | Path, value: Any) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(jsonable(value), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target


def load_problem_bundle(
    path: str | Path, *, study_dir: str | Path | None = None,
) -> tuple[GeneratedProblem, EvidencePacket]:
    bundle_path = Path(path).resolve()
    data = json.loads(bundle_path.read_text(encoding="utf-8"))
    raw_problem = data["problem"]
    rubric = tuple(
        RubricCriterion(
            criterion_id=item["criterion_id"],
            description=item["description"],
            max_points=float(item["max_points"]),
            levels=tuple(
                RubricLevel(
                    level_id=level["level_id"],
                    description=level["description"],
                    multiplier=float(level["multiplier"]),
                )
                for level in item["levels"]
            ),
        )
        for item in raw_problem["rubric"]
    )
    problem = GeneratedProblem(
        problem_id=raw_problem["problem_id"],
        problem_type=ProblemType(raw_problem["problem_type"]),
        statement=raw_problem["statement"],
        solution_outline=raw_problem["solution_outline"],
        evidence_ids=tuple(raw_problem["evidence_ids"]),
        rubric=rubric,
        evidence_packet_id=raw_problem["evidence_packet_id"],
        evidence_packet_hash=raw_problem["evidence_packet_hash"],
        manual_review=bool(raw_problem.get("manual_review", False)),
        review_reasons=tuple(raw_problem.get("review_reasons", [])),
    )
    try:
        packet = EvidencePacket.model_validate(data["evidence"])
    except ValidationError as exc:
        messages = "; ".join(str(item["msg"]) for item in exc.errors())
        raise EvidenceIntegrityError(messages) from exc
    if problem.evidence_packet_id != packet.packet_id:
        raise EvidenceIntegrityError("problem packet id mismatch")
    if problem.evidence_packet_hash != packet.computed_sha256():
        raise EvidenceIntegrityError("problem packet hash mismatch")
    root = Path(study_dir).resolve() if study_dir is not None else None
    if root is None:
        root = next(
            (parent for parent in bundle_path.parents if (parent / "generations").is_dir()),
            None,
        )
    if root is None:
        raise EvidenceIntegrityError("pinned corpus generation root cannot be resolved")
    generation = root / "generations" / packet.corpus_generation
    if not generation.is_dir():
        raise EvidenceIntegrityError(
            f"pinned corpus generation is missing: {packet.corpus_generation}"
        )
    manifest_path = generation / "manifest.json"
    if not manifest_path.is_file():
        raise EvidenceIntegrityError("pinned corpus generation has no manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recorded = manifest.get("digest")
    actual = str(recorded) if recorded is not None else stable_hash(manifest)
    if actual != packet.corpus_manifest_sha256:
        raise EvidenceIntegrityError("pinned corpus manifest digest mismatch")
    return problem, packet
