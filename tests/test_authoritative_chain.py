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


def test_authoritative_chain_export_embargo():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    lineage = result["evidence_lineage"]
    exceptions = result["exception_records"]
    trust_record = result["trust_record"]
    ledger = result["decision_ledger"]
    audit = result["audit_package"]
    export = result["export_package"]

    assert len(exceptions) == 1
    assert result["embargo"] is True
    assert trust_record.trust_classification == "EXPORT_EMBARGO"
    assert export is None

    assert engine.exception_record_repository.get(exceptions[0].exception_id) == exceptions[0]
    assert engine.evidence_lineage_repository.get(lineage.lineage_id) == lineage
    assert engine.trust_record_repository.get(trust_record.trust_record_id) == trust_record
    assert engine.decision_ledger_repository.get(ledger.decision_id) == ledger
    assert engine.audit_package_repository.get(audit.audit_package_id) == audit