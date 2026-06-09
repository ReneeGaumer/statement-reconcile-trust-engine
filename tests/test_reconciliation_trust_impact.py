from datetime import UTC, datetime

from trust_engine.application.trust_engine import TrustEngine
from trust_engine.domain.authoritative_models import (
    RuleApprovalRecord,
    RuleGovernanceRecord,
    RuleVersionRecord,
)


def authorize_engine_rule_version(engine):
    rule_version_reference = engine.policy.RULE_VERSION_REFERENCE

    engine.rule_version_repository.save(
        RuleVersionRecord(
            rule_version_reference,
            "TRUST_MODEL_RULES",
            "ACTIVE",
            datetime.now(UTC),
            "RULE_FP",
            None,
        )
    )
    engine.rule_approval_repository.save(
        RuleApprovalRecord(
            "APPROVAL-001",
            rule_version_reference,
            "GOVERNANCE_AUTHORITY",
            datetime.now(UTC),
            "APPROVED",
        )
    )
    engine.rule_governance_repository.save(
        RuleGovernanceRecord(
            "GOV-001",
            rule_version_reference,
            "APPROVAL-001",
            "AUTHORIZED",
            datetime.now(UTC),
            "GOVERNANCE_AUTHORITY",
            "Approved rule version authorized for governed trust execution.",
        )
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