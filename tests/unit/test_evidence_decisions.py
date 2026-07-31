from ai_math_study.domain.evidence import EvidenceEntry, EvidencePacket
from ai_math_study.domain.problems import evidence_decision


def _packet(*, verification: str = "verified", uncertain: bool = False) -> EvidencePacket:
    entry = EvidenceEntry(
        evidence_id="E01", span_id="c1", source_key="lftp.pdf",
        source_version_sha256="a" * 64, content_sha256="b" * 64,
        exact_excerpt="formula", authority="primary_text", corpus_tier="core",
        verification_state=verification, evidence_type="visual_formula",
        formula_uncertain=uncertain, locator_label="Ch1 p.8",
    )
    return EvidencePacket.freeze(
        "m" * 64, [entry], corpus_generation="gen-" + "1" * 64
    )


def test_provisional_and_manual_review_block_mastery_and_answer_release() -> None:
    provisional = evidence_decision(_packet(verification="unverified"))
    assert not provisional.may_advance_mastery
    assert not provisional.may_release_answer
    assert provisional.manual_review


def test_formula_uncertain_cannot_be_sole_deduction_evidence() -> None:
    decision = evidence_decision(_packet(uncertain=True), deduction_evidence_ids=("E01",))
    assert not decision.may_apply_deduction
    assert "formula_uncertain" in " ".join(decision.reasons)


def test_verified_certain_primary_evidence_allows_progress() -> None:
    decision = evidence_decision(_packet(), deduction_evidence_ids=("E01",))
    assert decision.may_apply_deduction
    assert decision.may_advance_mastery
    assert decision.may_release_answer
