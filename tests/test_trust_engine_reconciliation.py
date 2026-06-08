from trust_engine.application.trust_engine import TrustEngine
from trust_engine.reconciliation.reconciliation_status import ReconciliationStatus


def test_trust_engine_persists_reconciliation_records_with_trust_result():
    engine = TrustEngine()

    result = engine.determine_trust_with_reconciliation(
        evidence_count=10,
        severities=[],
        source_document_reference="statement.pdf",
        reconciliation_inputs=[
            {
                "field_name": "ending_balance",
                "expected_value": "1000.00",
                "actual_value": "1000.00",
            }
        ],
    )

    reconciliation_record = result["reconciliation_records"][0]

    assert reconciliation_record.status == ReconciliationStatus.MATCH.value
    assert result["reconciliation_record_references"] == [
        reconciliation_record.reconciliation_id
    ]
    assert (
        engine.reconciliation_record_repository.get(
            reconciliation_record.reconciliation_id
        )
        == reconciliation_record
    )
    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"


def test_trust_engine_preserves_reconciliation_mismatch_without_silent_correction():
    engine = TrustEngine()

    result = engine.determine_trust_with_reconciliation(
        evidence_count=10,
        severities=[],
        source_document_reference="statement.pdf",
        reconciliation_inputs=[
            {
                "field_name": "ending_balance",
                "expected_value": "$1,000.00",
                "actual_value": "1000.00",
            }
        ],
    )

    reconciliation_record = result["reconciliation_records"][0]

    assert reconciliation_record.expected_value == "$1,000.00"
    assert reconciliation_record.actual_value == "1000.00"
    assert reconciliation_record.status == ReconciliationStatus.UNRECONCILABLE.value
    assert result["trust_record"].trust_classification == "EXPORT_WITH_WARNINGS"


def test_trust_engine_supports_multiple_reconciliation_records():
    engine = TrustEngine()

    result = engine.determine_trust_with_reconciliation(
        evidence_count=10,
        severities=[],
        source_document_reference="statement.pdf",
        reconciliation_inputs=[
            {
                "field_name": "beginning_balance",
                "expected_value": "900.00",
                "actual_value": "900.00",
            },
            {
                "field_name": "ending_balance",
                "expected_value": "1000.00",
                "actual_value": "999.99",
                "tolerance": "0.01",
            },
        ],
    )

    assert len(result["reconciliation_records"]) == 2
    assert len(result["reconciliation_record_references"]) == 2
    assert result["reconciliation_records"][0].status == ReconciliationStatus.MATCH.value
    assert (
        result["reconciliation_records"][1].status
        == ReconciliationStatus.MATCH_WITH_TOLERANCE.value
    )


def test_trust_engine_creates_reconciliation_decision_link():
    engine = TrustEngine()

    result = engine.determine_trust_with_reconciliation(
        evidence_count=10,
        severities=[],
        source_document_reference="statement.pdf",
        reconciliation_inputs=[
            {
                "field_name": "ending_balance",
                "expected_value": "1000.00",
                "actual_value": "1000.00",
            }
        ],
    )

    link = result["reconciliation_decision_link"]

    assert result["reconciliation_decision_link_reference"] == (
        link.reconciliation_decision_link_id
    )
    assert link.trust_record_reference == result["trust_record"].trust_record_id
    assert link.decision_explanation_reference == (
        result["decision_explanation"].decision_explanation_id
    )
    assert link.reconciliation_record_references == (
        result["reconciliation_record_references"]
    )
    assert link.source_document_reference == "statement.pdf"
    assert link.rule_reference == engine.policy.RECONCILIATION_TRUST_IMPACT_RULE
    assert (
        engine.reconciliation_decision_link_repository.get(
            link.reconciliation_decision_link_id
        )
        == link
    )