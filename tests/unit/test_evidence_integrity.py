from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_math_study.domain.evidence import EvidenceEntry, EvidenceIntegrityError, EvidencePacket
from ai_math_study.domain.problems import (
    GeneratedProblem,
    ProblemType,
    RubricCriterion,
    RubricLevel,
    packet_digest,
)
from ai_math_study.serde import load_problem_bundle, write_json


def _entry(**changes: object) -> EvidenceEntry:
    values = {
        "evidence_id": "E01",
        "span_id": "claim-1",
        "source_key": "lftp.pdf",
        "source_version_sha256": "a" * 64,
        "content_sha256": "b" * 64,
        "exact_excerpt": "Assume independent bounded observations.",
        "authority": "primary_text",
        "corpus_tier": "core",
        "verification_state": "source-aligned",
        "evidence_type": "extracted_text",
        "formula_uncertain": False,
        "locator_label": "Ch 1 | print p.8 | PDF p.24",
    }
    values.update(changes)
    return EvidenceEntry(**values)  # type: ignore[arg-type]


def _bundle(packet: EvidencePacket) -> dict[str, object]:
    levels = (RubricLevel("full", "correct", 1), RubricLevel("none", "wrong", 0))
    problem = GeneratedProblem(
        "p1", ProblemType.PROOF, "Prove", "Outline", ("E01",),
        (RubricCriterion("logic", "logic", 100, levels),),
        packet.packet_id, packet_digest(packet),
    )
    return {"problem": problem, "evidence": packet}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("exact_excerpt", "changed"),
        ("authority", "user_note"),
        ("corpus_tier", "prerequisite"),
        ("verification_state", "contradicted"),
        ("evidence_type", "visual_formula"),
        ("formula_uncertain", True),
        ("locator_label", "fake page"),
    ],
)
def test_packet_digest_covers_all_evidence_semantics(field: str, value: object) -> None:
    packet = EvidencePacket.freeze("m" * 64, [_entry()], corpus_generation="gen-" + "1" * 64)
    changed = packet.model_copy(
        update={"entries": [packet.entries[0].model_copy(update={field: value})]}
    )
    assert packet_digest(changed) != packet_digest(packet)


def test_packet_digest_covers_entry_order() -> None:
    packet = EvidencePacket.freeze(
        "m" * 64,
        [_entry(), _entry(evidence_id="E02", span_id="claim-2")],
        corpus_generation="gen-" + "1" * 64,
    )
    reversed_packet = packet.model_copy(update={"entries": list(reversed(packet.entries))})
    assert packet_digest(reversed_packet) != packet_digest(packet)


def test_load_rejects_forged_entry_and_packet(tmp_path: Path) -> None:
    packet = EvidencePacket.freeze("m" * 64, [_entry()], corpus_generation="gen-" + "1" * 64)
    path = write_json(tmp_path / "bundle.json", _bundle(packet))
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["evidence"]["entries"][0]["exact_excerpt"] = "forged"
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(EvidenceIntegrityError, match="entry hash mismatch"):
        load_problem_bundle(path)


def test_load_rejects_forged_packet_hash(tmp_path: Path) -> None:
    packet = EvidencePacket.freeze("m" * 64, [_entry()], corpus_generation="gen-" + "1" * 64)
    path = write_json(tmp_path / "bundle.json", _bundle(packet))
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["evidence"]["packet_sha256"] = "0" * 64
    path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(EvidenceIntegrityError, match="packet hash mismatch"):
        load_problem_bundle(path)


def test_load_requires_pinned_generation_to_exist(tmp_path: Path) -> None:
    packet = EvidencePacket.freeze("m" * 64, [_entry()], corpus_generation="gen-" + "1" * 64)
    path = write_json(tmp_path / "bundle.json", _bundle(packet))

    with pytest.raises(EvidenceIntegrityError, match="pinned corpus generation"):
        load_problem_bundle(path, study_dir=tmp_path / ".study")

    generation = tmp_path / ".study" / "generations" / packet.corpus_generation
    generation.mkdir(parents=True)
    (generation / "manifest.json").write_text(
        json.dumps({"digest": packet.corpus_manifest_sha256}), encoding="utf-8"
    )
    loaded_problem, loaded_packet = load_problem_bundle(path, study_dir=tmp_path / ".study")
    assert loaded_problem.problem_id == "p1"
    assert loaded_packet.corpus_generation == packet.corpus_generation
