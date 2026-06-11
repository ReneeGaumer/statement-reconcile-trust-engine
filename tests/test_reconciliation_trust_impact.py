from trust_engine.application.trust_engine import TrustEngine
from tests.governance_test_helpers import (
    authorize_engine_rule_version,
    complete_evidence_lineage_metadata,
)


def test_reconciliation_mismatch_creates_trust_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust_with_reconciliation(
        evidence_count=10,
        severities=[],
        source_document_reference="statement.pdf",
        reconciliation_inputs=[
            {
                "field_name": "ending_balance",
                "expected_value": "1000.00",
                "actual_value": "900.00",
            }
        ],
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    reconciliation_record = result["reconciliation_records"][0]
    exception_record = result["exception_records"][0]

    assert reconciliation_record.status == "MISMATCH"
    assert reconciliation_record.field_name == "ending_balance"
    assert reconciliation_record.expected_value == "1000.00"
    assert reconciliation_record.actual_value == "900.00"

    assert len(result["exception_records"]) == 1
    assert exception_record.severity == "WARNING"
    assert exception_record.field_name == reconciliation_record.field_name
    assert exception_record.original_value == reconciliation_record.actual_value
    assert exception_record.expected_value == reconciliation_record.expected_value
    assert result["exception_penalty"] == 15.0
    assert result["trust_record"].exception_count == 1
    assert result["trust_record"].exception_penalty == 15.0
    assert result["trust_record"].trust_score == 85.0
    assert result["trust_record"].trust_classification == "EXPORT_WITH_WARNINGS"


def test_reconciliation_match_does_not_create_trust_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

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
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    assert result["reconciliation_records"][0].status == "MATCH"
    assert result["exception_records"] == []
    assert result["exception_penalty"] == 0
    assert result["trust_record"].trust_score == 100.0
    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"


def test_reconciliation_unreconcilable_creates_trust_exception_without_correction():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

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
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    reconciliation_record = result["reconciliation_records"][0]
    exception_record = result["exception_records"][0]

    assert reconciliation_record.status == "UNRECONCILABLE"
    assert reconciliation_record.expected_value == "$1,000.00"
    assert reconciliation_record.actual_value == "1000.00"

    assert len(result["exception_records"]) == 1
    assert exception_record.severity == "WARNING"
    assert exception_record.field_name == reconciliation_record.field_name
    assert exception_record.original_value == reconciliation_record.actual_value
    assert exception_record.expected_value == reconciliation_record.expected_value
    assert result["trust_record"].trust_classification == "EXPORT_WITH_WARNINGS"


def test_reconciliation_mismatch_exception_is_field_specific_and_preserves_values():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust_with_reconciliation(
        evidence_count=10,
        severities=[],
        source_document_reference="statement.pdf",
        reconciliation_inputs=[
            {
                "field_name": "ending_balance",
                "expected_value": "1000.00",
                "actual_value": "900.00",
            }
        ],
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    reconciliation_record = result["reconciliation_records"][0]
    exception_record = result["exception_records"][0]

    assert exception_record.severity == "WARNING"
    assert exception_record.field_name == reconciliation_record.field_name
    assert exception_record.original_value == reconciliation_record.actual_value
    assert exception_record.expected_value == reconciliation_record.expected_value
    assert exception_record.source_reference == reconciliation_record.reconciliation_id
    assert exception_record.rule_name == engine.policy.RECONCILIATION_TRUST_IMPACT_RULE
    assert "MISMATCH" in exception_record.exception_reason
    assert "ending_balance" in exception_record.exception_reason