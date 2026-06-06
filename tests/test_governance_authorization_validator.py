from datetime import datetime, UTC

from trust_engine.application.governance_authorization_validator import GovernanceAuthorizationValidator
from trust_engine.domain.authoritative_models import RuleVersionRecord, RuleApprovalRecord, RuleGovernanceRecord


def test_governance_authorization_validator_authorizes_valid_chain():
    rule = RuleVersionRecord("TRUST_MODEL_RULES_V1", "TRUST_MODEL_RULES", "ACTIVE", datetime.now(UTC), "RULE_FP", None)
    approval = RuleApprovalRecord("APPROVAL-001", "TRUST_MODEL_RULES_V1", "GOVERNANCE_AUTHORITY", datetime.now(UTC), "APPROVED")
    governance = RuleGovernanceRecord("GOV-001", "TRUST_MODEL_RULES_V1", "APPROVAL-001", "AUTHORIZED", datetime.now(UTC), "GOVERNANCE_AUTHORITY", "Approved rule version authorized for governed trust execution")

    validator = GovernanceAuthorizationValidator()

    result = validator.is_authorized(rule, approval, governance)

    assert result is True


def test_governance_authorization_validator_rejects_unapproved_chain():
    rule = RuleVersionRecord("TRUST_MODEL_RULES_V1", "TRUST_MODEL_RULES", "ACTIVE", datetime.now(UTC), "RULE_FP", None)
    approval = RuleApprovalRecord("APPROVAL-001", "TRUST_MODEL_RULES_V1", "GOVERNANCE_AUTHORITY", datetime.now(UTC), "REJECTED")
    governance = RuleGovernanceRecord("GOV-001", "TRUST_MODEL_RULES_V1", "APPROVAL-001", "AUTHORIZED", datetime.now(UTC), "GOVERNANCE_AUTHORITY", "Approved rule version authorized for governed trust execution")

    validator = GovernanceAuthorizationValidator()

    result = validator.is_authorized(rule, approval, governance)

    assert result is False


def test_governance_authorization_validator_rejects_mismatched_approval_reference():
    rule = RuleVersionRecord("TRUST_MODEL_RULES_V1", "TRUST_MODEL_RULES", "ACTIVE", datetime.now(UTC), "RULE_FP", None)
    approval = RuleApprovalRecord("APPROVAL-999", "TRUST_MODEL_RULES_V1", "GOVERNANCE_AUTHORITY", datetime.now(UTC), "APPROVED")
    governance = RuleGovernanceRecord("GOV-001", "TRUST_MODEL_RULES_V1", "APPROVAL-001", "AUTHORIZED", datetime.now(UTC), "GOVERNANCE_AUTHORITY", "Approved rule version authorized for governed trust execution")

    validator = GovernanceAuthorizationValidator()

    result = validator.is_authorized(rule, approval, governance)

    assert result is False
