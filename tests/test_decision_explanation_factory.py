from trust_engine.application.decision_explanation_factory import DecisionExplanationFactory


def test_decision_explanation_factory():
    factory = DecisionExplanationFactory()
    record = factory.create("TR-001", 10, 1, 50.0, True, 50.0, "EXPORT_EMBARGO", ["EVIDENCE_LINEAGE_CREATED", "EXCEPTION_RULES_EVALUATED", "TRUST_SCORE_CALCULATED", "EXPORT_EMBARGO_EVALUATED", "TRUST_CLASSIFICATION_ASSIGNED"])

    assert record.decision_explanation_id
    assert record.trust_record_reference == "TR-001"
    assert record.evidence_count == 10
    assert record.exception_count == 1
    assert record.exception_penalty == 50.0
    assert record.embargo is True
    assert record.trust_score == 50.0
    assert record.trust_classification == "EXPORT_EMBARGO"
    assert record.decision_path == ["EVIDENCE_LINEAGE_CREATED", "EXCEPTION_RULES_EVALUATED", "TRUST_SCORE_CALCULATED", "EXPORT_EMBARGO_EVALUATED", "TRUST_CLASSIFICATION_ASSIGNED"]
    assert record.created_timestamp
