from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity


def test_export_package_id_reconstructs_full_authoritative_chain():
    engine = TrustEngine()
    result = engine.determine_trust(10, [], "statement.pdf")

    export_package_id = result["export_package"].export_package_id
    export_package = engine.export_package_repository.get(export_package_id)
    audit_package = engine.audit_package_repository.get(export_package.audit_package_reference)
    trust_record = engine.trust_record_repository.get(audit_package.trust_record_reference)
    evidence_lineage = engine.evidence_lineage_repository.get(
        audit_package.evidence_lineage_reference
    )
    decision_ledger = engine.decision_ledger_repository.get(
        audit_package.decision_ledger_reference
    )
    decision_explanation = engine.decision_explanation_repository.get(
        audit_package.decision_explanation_reference
    )

    assert export_package == result["export_package"]
    assert audit_package == result["audit_package"]
    assert trust_record == result["trust_record"]
    assert evidence_lineage == result["evidence_lineage"]
    assert decision_ledger == result["decision_ledger"]
    assert decision_explanation == result["decision_explanation"]

    assert decision_ledger.trust_record_reference == trust_record.trust_record_id
    assert decision_ledger.decision_explanation_reference == (
        decision_explanation.decision_explanation_id
    )
    assert decision_ledger.rule_version_reference == "TRUST_MODEL_RULES_V1"
    assert decision_ledger.decision_rationale
    assert decision_ledger.evidence_references == [evidence_lineage.lineage_id]
    assert decision_ledger.exception_references == []
    assert decision_ledger.trust_score == trust_record.trust_score
    assert decision_ledger.trust_classification == trust_record.trust_classification
    assert decision_ledger.decision_outcome == trust_record.trust_classification
    assert decision_ledger.decision_timestamp
    assert decision_ledger.created_timestamp

    assert decision_explanation.trust_record_reference == trust_record.trust_record_id
    assert decision_explanation.evidence_count == trust_record.evidence_count
    assert decision_explanation.exception_count == trust_record.exception_count
    assert decision_explanation.exception_penalty == trust_record.exception_penalty
    assert decision_explanation.embargo == trust_record.embargo
    assert decision_explanation.trust_score == trust_record.trust_score
    assert decision_explanation.trust_classification == trust_record.trust_classification
    assert decision_explanation.exception_record_references == []
    assert decision_explanation.decision_path

    required_steps = {
        "EVIDENCE_LINEAGE_CREATED",
        "EXCEPTION_RULES_EVALUATED",
        "TRUST_SCORE_CALCULATED",
        "EXPORT_EMBARGO_EVALUATED",
        "TRUST_CLASSIFICATION_ASSIGNED",
    }
    observed_steps = {step["step"] for step in decision_explanation.decision_path}

    assert required_steps == observed_steps
    for step in decision_explanation.decision_path:
        assert step["rule"]
        assert "inputs" in step
        assert "output" in step


def test_export_embargo_has_no_export_package_but_preserves_audit_chain():
    engine = TrustEngine()
    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    audit_package = result["audit_package"]
    trust_record = result["trust_record"]
    decision_ledger = result["decision_ledger"]
    decision_explanation = result["decision_explanation"]
    evidence_lineage = result["evidence_lineage"]
    exceptions = result["exception_records"]

    assert result["embargo"] is True
    assert result["export_package"] is None
    assert trust_record.trust_classification == "EXPORT_EMBARGO"

    assert engine.audit_package_repository.get(audit_package.audit_package_id) == audit_package
    assert engine.trust_record_repository.get(trust_record.trust_record_id) == trust_record
    assert engine.decision_ledger_repository.get(decision_ledger.decision_id) == decision_ledger
    assert engine.decision_explanation_repository.get(
        decision_explanation.decision_explanation_id
    ) == decision_explanation
    assert engine.evidence_lineage_repository.get(evidence_lineage.lineage_id) == evidence_lineage

    assert decision_ledger.trust_record_reference == trust_record.trust_record_id
    assert decision_ledger.decision_explanation_reference == (
        decision_explanation.decision_explanation_id
    )
    assert decision_ledger.rule_version_reference == "TRUST_MODEL_RULES_V1"
    assert decision_ledger.evidence_references == [evidence_lineage.lineage_id]
    assert decision_ledger.exception_references == [
        record.exception_id for record in exceptions
    ]
    assert decision_ledger.trust_classification == "EXPORT_EMBARGO"
    assert decision_ledger.decision_outcome == "EXPORT_EMBARGO"

    assert decision_explanation.embargo is True
    assert decision_explanation.trust_classification == "EXPORT_EMBARGO"
    assert decision_explanation.exception_record_references == [
        record.exception_id for record in exceptions
    ]

    observed_steps = {step["step"] for step in decision_explanation.decision_path}
    assert "EXPORT_EMBARGO_EVALUATED" in observed_steps
    assert "TRUST_CLASSIFICATION_ASSIGNED" in observed_steps