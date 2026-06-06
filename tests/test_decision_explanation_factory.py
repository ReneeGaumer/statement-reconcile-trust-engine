from trust_engine.application.decision_explanation_factory import DecisionExplanationFactory


def test_decision_explanation_factory():
    factory = DecisionExplanationFactory()
    record = factory.create("TR-001", 10, 1, 50.0, True, 50.0, "EXPORT_EMBARGO", [{"step": "TRUST_SCORE_CALCULATED", "rule": "EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY", "inputs": {"evidence_count": 10, "exception_penalty": 50.0}, "output": 50.0}])

    assert record.decision_explanation_id
    assert record.trust_record_reference == "TR-001"
    assert record.exception_record_references == []
    assert record.evidence_count == 10
    assert record.exception_count == 1
    assert record.exception_penalty == 50.0
    assert record.embargo is True
    assert record.trust_score == 50.0
    assert record.trust_classification == "EXPORT_EMBARGO"
    assert record.decision_path[0]["step"] == "TRUST_SCORE_CALCULATED"
    assert record.decision_path[0]["rule"] == "EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY"
    assert record.decision_path[0]["inputs"]["evidence_count"] == 10
    assert record.decision_path[0]["output"] == 50.0
    assert record.created_timestamp
