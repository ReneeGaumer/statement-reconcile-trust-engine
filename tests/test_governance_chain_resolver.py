from datetime import datetime, UTC

from trust_engine.application.governance_chain_resolver import GovernanceChainResolver
from trust_engine.domain.authoritative_models import RuleVersionRecord, RuleApprovalRecord, RuleGovernanceRecord
from trust_engine.infrastructure.rule_version_repository import RuleVersionRepository
from trust_engine.infrastructure.rule_approval_repository import RuleApprovalRepository
from trust_engine.infrastructure.rule_governance_repository import RuleGovernanceRepository


def test_governance_chain_resolver_authorizes_stored_chain():
    rule_repo = RuleVersionRepository()
    approval_repo = RuleApprovalRepository()
    governance_repo = RuleGovernanceRepository()

    rule = RuleVersionRecord("TRUST_MODEL_RULES_V1", "TRUST_MODEL_RULES", "ACTIVE", datetime.now(UTC), "RULE_FP", None)
    approval = RuleApprovalRecord("APPROVAL-001", "TRUST_MODEL_RULES_V1", "GOVERNANCE_AUTHORITY", datetime.now(UTC), "APPROVED")
    governance = RuleGovernanceRecord("GOV-001", "TRUST_MODEL_RULES_V1", "APPROVAL-001", "AUTHORIZED", datetime.now(UTC), "GOVERNANCE_AUTHORITY", "Approved rule version authorized for governed trust execution")

    rule_repo.save(rule)
    approval_repo.save(approval)
    governance_repo.save(governance)

    resolver = GovernanceChainResolver(rule_repo, approval_repo, governance_repo)

    result = resolver.is_rule_authorized("TRUST_MODEL_RULES_V1")

    assert result is True


def test_governance_chain_resolver_rejects_missing_governance_record():
    rule_repo = RuleVersionRepository()
    approval_repo = RuleApprovalRepository()
    governance_repo = RuleGovernanceRepository()

    rule = RuleVersionRecord("TRUST_MODEL_RULES_V1", "TRUST_MODEL_RULES", "ACTIVE", datetime.now(UTC), "RULE_FP", None)
    approval = RuleApprovalRecord("APPROVAL-001", "TRUST_MODEL_RULES_V1", "GOVERNANCE_AUTHORITY", datetime.now(UTC), "APPROVED")

    rule_repo.save(rule)
    approval_repo.save(approval)

    resolver = GovernanceChainResolver(rule_repo, approval_repo, governance_repo)

    result = resolver.is_rule_authorized("TRUST_MODEL_RULES_V1")

    assert result is False
