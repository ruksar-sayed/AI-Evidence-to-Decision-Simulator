from decision_engine import evaluate_decision
from conflict_detector import detect_conflicts


def test_invalid_evidence_id_is_rejected():
    result = evaluate_decision(
        conclusion="The quantity discrepancy is unresolved.",
        supporting_ids=["E999"],
        counter_ids=[],
        confidence=3,
        next_action="Review delivery documentation.",
        available_ids={"E001", "E002", "E003"}
    )

    assert "E999" in result["invalid_ids"]
    assert "E999" not in result["valid_supporting_ids"]


def test_empty_conclusion_gets_no_conclusion_marks():
    result = evaluate_decision(
        conclusion="",
        supporting_ids=[],
        counter_ids=[],
        confidence=3,
        next_action="Request the delivery receipt.",
        available_ids={"E001"}
    )

    assert result["score"] == 35


def test_no_evidence_means_no_detected_conflicts():
    result = detect_conflicts([])

    assert result == []