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


def test_trust_engine_rejects_missing_governance_before_trust_artifacts():
    engine = TrustEngine()

    try:
        engine.determine_trust(10, [], "statement.pdf")
        raise AssertionError("unauthorized governance should stop trust execution")
    except PermissionError as error:
        assert "unauthorized rule version" in str(error)

    assert engine.trust_record_repository.all() == []
    assert engine.decision_ledger_repository.all() == []
    assert engine.audit_package_repository.all() == []
    assert engine.export_package_repository.all() == []


def test_trust_engine_allows_export_when_rule_version_is_authorized():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [], "statement.pdf")

    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"
    assert result["decision_ledger"].rule_version_reference == (
        engine.policy.RULE_VERSION_REFERENCE
    )
    assert result["audit_package"].rule_version_references == [
        engine.policy.RULE_VERSION_REFERENCE
    ]
    assert result["export_package"] is not None