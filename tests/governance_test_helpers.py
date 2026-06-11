from datetime import UTC, datetime

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


def complete_evidence_lineage_metadata():
    return {
        "source_location": "bank-portal",
        "page_reference": "page-1",
        "acquisition_method": "UPLOAD",
        "evidence_hash": "hash-001",
        "chain_of_custody": ["uploaded-by-user"],
        "evidence_type": "BANK_STATEMENT",
        "evidence_status": "CAPTURED",
    }