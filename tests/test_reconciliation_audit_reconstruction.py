from trust_engine.application.trust_engine import TrustEngine
from trust_engine.reconciliation.reconciliation_status import ReconciliationStatus


def test_reconciliation_decision_link_reconstructs_trust_and_reconciliation_chain():
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

    link_id = result["reconciliation_decision_link_reference"]
    link = engine.reconciliation_decision_link_repository.get(link_id)

    trust_record = engine.trust_record_repository.get(link.trust_record_reference)
    decision_explanation = engine.decision_explanation_repository.get(
        link.decision_explanation_reference
    )
    reconciliation_records = [
        engine.reconciliation_record_repository.get(reconciliation_record_reference)
        for reconciliation_record_reference in link.reconciliation_record_references
    ]

    assert link == result["reconciliation_decision_link"]
    assert trust_record == result["trust_record"]
    assert decision_explanation == result["decision_explanation"]
    assert reconciliation_records == result["reconciliation_records"]

    assert link.trust_record_reference == trust_record.trust_record_id
    assert (
        link.decision_explanation_reference
        == decision_explanation.decision_explanation_id
    )
    assert link.reconciliation_record_references == [
        record.reconciliation_id for record in reconciliation_records
    ]
    assert link.source_document_reference == "statement.pdf"
    assert link.rule_reference == "RECONCILIATION_RECORD_REFERENCES_CAPTURED"

    assert reconciliation_records[0].status == ReconciliationStatus.MATCH.value
    assert (
        reconciliation_records[1].status
        == ReconciliationStatus.MATCH_WITH_TOLERANCE.value
    )
    assert trust_record.trust_classification == "CLEAN_EXPORT"


def test_reconciliation_decision_link_reconstructs_mismatch_without_correction():
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

    link = engine.reconciliation_decision_link_repository.get(
        result["reconciliation_decision_link_reference"]
    )
    reconciliation_record = engine.reconciliation_record_repository.get(
        link.reconciliation_record_references[0]
    )

    assert reconciliation_record.expected_value == "$1,000.00"
    assert reconciliation_record.actual_value == "1000.00"
    assert reconciliation_record.status == ReconciliationStatus.UNRECONCILABLE.value
    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"