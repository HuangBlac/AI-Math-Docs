from ai_math_study.domain.evidence import EvidenceEntry, EvidencePacket
from ai_math_study.domain.problems import (
    GeneratedProblem, ProblemType, RubricCriterion, RubricLevel, content_digest, packet_digest,
)
from ai_math_study.grader import EvidenceGrader
from ai_math_study.providers import FakeProvider


def test_forged_level_cannot_create_points():
    entry = EvidenceEntry(
        evidence_id="E01", span_id="s", source_key="lftp", source_version_sha256="v",
        content_sha256=content_digest("source"), exact_excerpt="source", authority="primary_text",
        locator_label="p.1",
    )
    evidence = EvidencePacket.freeze("manifest", [entry])
    rubric = (RubricCriterion("c", "correct", 100, (RubricLevel("yes", "yes", 1), RubricLevel("no", "no", 0))),)
    problem = GeneratedProblem(
        "p", ProblemType.PROOF, "s", "o", ("E01",), rubric,
        evidence.packet_id, packet_digest(evidence),
    )
    malicious = {"assessments": [{"criterion_id": "c", "level_id": "SUPER_1000",
        "answer_location": "", "reason": "", "correction": "", "evidence_ids": ["E01"]}],
        "overall_feedback": "", "fatal_misconceptions": [], "review_flags": []}
    report = EvidenceGrader(FakeProvider([malicious])).grade(problem, "answer", evidence)
    assert report.score == 0
    assert report.manual_review
