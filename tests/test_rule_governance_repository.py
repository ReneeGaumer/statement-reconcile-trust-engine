from datetime import datetime, UTC

from trust_engine.domain.authoritative_models import RuleGovernanceRecord
from trust_engine.infrastructure.rule_governance_repository import RuleGovernanceRepository


def test_rule_governance_repository_stores_authoritative_governance_chain():
    record = RuleGovernanceRecord(
        governance_id="GOV-001",
        rule_version_reference="TRUST_MODEL_RULES_V1",
        approval_reference="APPROVAL-001",
        governance_status="AUTHORIZED",
        effective_timestamp=datetime.now(UTC),
        authorized_by="GOVERNANCE_AUTHORITY",
        governance_reason="Approved rule version authorized for governed trust execution",
    )

    repo = RuleGovernanceRepository()
    repo.save(record)

    loaded = repo.get("GOV-001")

    assert loaded == record
    assert loaded.rule_version_reference == "TRUST_MODEL_RULES_V1"
    assert loaded.approval_reference == "APPROVAL-001"
    assert loaded.governance_status == "AUTHORIZED"
    assert loaded.authorized_by == "GOVERNANCE_AUTHORITY"
