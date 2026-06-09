from datetime import datetime, UTC

from trust_engine.domain.authoritative_models import RuleApprovalRecord
from trust_engine.infrastructure.rule_approval_repository import RuleApprovalRepository


def test_rule_approval_repository_stores_rule_approval_authority():
    record = RuleApprovalRecord(
        approval_id="APPROVAL-001",
        rule_version_reference="TRUST_MODEL_RULES_V1",
        approver="GOVERNANCE_AUTHORITY",
        approval_timestamp=datetime.now(UTC),
        approval_status="APPROVED",
    )

    repo = RuleApprovalRepository()
    repo.save(record)

    loaded = repo.get("APPROVAL-001")

    assert loaded == record
    assert loaded.rule_version_reference == "TRUST_MODEL_RULES_V1"
    assert loaded.approval_status == "APPROVED"
