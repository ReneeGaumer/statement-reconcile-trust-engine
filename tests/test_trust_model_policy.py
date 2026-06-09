from datetime import UTC, datetime

from trust_engine.application.trust_engine import TrustEngine
from trust_engine.application.trust_model_policy import TrustModelPolicy
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


def test_trust_model_policy_defines_authoritative_penalties():
    policy = TrustModelPolicy()

    assert policy.penalty_for(Severity.INFO) == 5.0
    assert policy.penalty_for(Severity.WARNING) == 15.0
    assert policy.penalty_for(Severity.HIGH) == 40.0
    assert policy.penalty_for(Severity.CRITICAL) == 100.0


def test_trust_model_policy_defines_authoritative_classifications():
    policy = TrustModelPolicy()

    assert policy.classify(100.0, False) == "CLEAN_EXPORT"
    assert policy.classify(99.99, False) == "EXPORT_WITH_WARNINGS"
    assert policy.classify(85.0, False) == "EXPORT_WITH_WARNINGS"
    assert policy.classify(84.99, False) == "PARTIAL_EXPORT"
    assert policy.classify(60.0, False) == "PARTIAL_EXPORT"
    assert policy.classify(59.99, False) == "UNSAFE_EXPORT"
    assert policy.classify(1.0, False) == "UNSAFE_EXPORT"
    assert policy.classify(0.99, False) == "UNSAFE_EXPORT"


def test_trust_model_policy_embargo_overrides_score():
    policy = TrustModelPolicy()

    assert policy.classify(100.0, True) == "EXPORT_EMBARGO"


def test_trust_model_policy_embargo_rule_uses_critical_severity():
    policy = TrustModelPolicy()

    assert policy.should_embargo([Severity.WARNING]) is False
    assert policy.should_embargo([Severity.CRITICAL]) is True


def test_trust_engine_records_policy_rule_references_in_authoritative_chain():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [], "statement.pdf")
    policy = engine.policy

    trust_record = result["trust_record"]
    decision_ledger = result["decision_ledger"]
    decision_explanation = result["decision_explanation"]
    audit_package = result["audit_package"]

    assert trust_record.trust_calculation_rule == policy.SCORE_CALCULATION_RULE
    assert decision_ledger.rule_version_reference == policy.RULE_VERSION_REFERENCE
    assert audit_package.rule_version_references == [policy.RULE_VERSION_REFERENCE]

    rules_by_step = {
        step["step"]: step["rule"]
        for step in decision_explanation.decision_path
    }

    assert (
        rules_by_step["TRUST_POLICY_SOURCE_LOADED"]
        == "TRUST_MODEL_POLICY_SOURCE_METADATA_CAPTURED"
    )
    assert rules_by_step["EXCEPTION_RULES_EVALUATED"] == policy.EXCEPTION_PENALTY_RULE
    assert rules_by_step["TRUST_SCORE_CALCULATED"] == policy.SCORE_CALCULATION_RULE
    assert rules_by_step["EXPORT_EMBARGO_EVALUATED"] == policy.EMBARGO_RULE
    assert rules_by_step["TRUST_CLASSIFICATION_ASSIGNED"] == policy.CLASSIFICATION_RULE

    outputs_by_step = {
        step["step"]: step["output"]
        for step in decision_explanation.decision_path
    }

    assert outputs_by_step["TRUST_POLICY_SOURCE_LOADED"] == policy.policy_source_metadata()