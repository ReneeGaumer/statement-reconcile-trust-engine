from datetime import UTC, datetime

from trust_engine.application.trust_engine import TrustEngine
from trust_engine.domain.authoritative_models import (
    RuleApprovalRecord,
    RuleGovernanceRecord,
    RuleVersionRecord,
)
from trust_engine.exceptions.severity import Severity


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


def test_trust_engine_exception_persistence():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10, [Severity.WARNING, Severity.CRITICAL], "statement.pdf"
    )

    exceptions = result["exception_records"]

    assert len(exceptions) == 2
    assert result["exception_penalty"] == 115.0
    assert exceptions[0].severity == "WARNING"
    assert exceptions[0].penalty == 15.0
    assert exceptions[0].source_reference == "statement.pdf"
    assert exceptions[0].field_name == "TRUST_SEVERITY"
    assert exceptions[0].original_value == "WARNING"
    assert exceptions[0].expected_value == "NO_EXCEPTION"
    assert exceptions[1].severity == "CRITICAL"
    assert exceptions[1].penalty == 100.0

    stored = engine.exception_record_repository.all()
    assert len(stored) == 2
    assert [record.exception_id for record in stored] == [
        record.exception_id for record in exceptions
    ]