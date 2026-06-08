from trust_engine.application.trust_engine import TrustEngine


def test_reconciliation_mismatch_creates_trust_exception():
    engine = TrustEngine()

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
    )

    reconciliation_record = result["reconciliation_records"][0]
    exception_record = result["exception_records"][0]

    assert reconciliation_record.status == "MISMATCH"
    assert reconciliation_record.field_name == "ending_balance"
    assert reconciliation_record.expected_value == "1000.00"
    assert reconciliation_record.actual_value == "900.00"

    assert len(result["exception_records"]) == 1
    assert exception_record.severity == "WARNING"
    assert exception_record.field_name == "TRUST_SEVERITY"
    assert exception_record.original_value == "WARNING"
    assert exception_record.expected_value == "NO_EXCEPTION"
    assert result["exception_penalty"] == 15.0
    assert result["trust_record"].exception_count == 1
    assert result["trust_record"].exception_penalty == 15.0
    assert result["trust_record"].trust_score == 85.0
    assert result["trust_record"].trust_classification == "EXPORT_WITH_WARNINGS"


def test_reconciliation_match_does_not_create_trust_exception():
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

    assert result["reconciliation_records"][0].status == "MATCH"
    assert result["exception_records"] == []
    assert result["exception_penalty"] == 0
    assert result["trust_record"].trust_score == 100.0
    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"


def test_reconciliation_unreconcilable_creates_trust_exception_without_correction():
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
    exception_record = result["exception_records"][0]

    assert reconciliation_record.status == "UNRECONCILABLE"
    assert reconciliation_record.expected_value == "$1,000.00"
    assert reconciliation_record.actual_value == "1000.00"

    assert len(result["exception_records"]) == 1
    assert exception_record.severity == "WARNING"
    assert exception_record.field_name == "TRUST_SEVERITY"
    assert exception_record.original_value == "WARNING"
    assert exception_record.expected_value == "NO_EXCEPTION"
    assert result["trust_record"].trust_classification == "EXPORT_WITH_WARNINGS"