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


def test_export_package_id_reconstructs_full_authoritative_chain():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [], "statement.pdf")

    export_package_id = result["export_package"].export_package_id
    export_package = engine.export_package_repository.get(export_package_id)
    audit_package = engine.audit_package_repository.get(export_package.audit_package_reference)
    trust_record = engine.trust_record_repository.get(audit_package.trust_record_reference)
    evidence_lineage = engine.evidence_lineage_repository.get(
        audit_package.evidence_lineage_reference
    )
    decision_ledger = engine.decision_ledger_repository.get(
        audit_package.decision_ledger_reference
    )
    decision_explanation = engine.decision_explanation_repository.get(
        audit_package.decision_explanation_reference
    )

    assert export_package == result["export_package"]
    assert audit_package == result["audit_package"]
    assert trust_record == result["trust_record"]
    assert evidence_lineage == result["evidence_lineage"]
    assert decision_ledger == result["decision_ledger"]
    assert decision_explanation == result["decision_explanation"]

    assert decision_ledger.trust_record_reference == trust_record.trust_record_id
    assert decision_ledger.decision_explanation_reference == (
        decision_explanation.decision_explanation_id
    )
    assert decision_ledger.rule_version_reference == engine.policy.RULE_VERSION_REFERENCE
    assert decision_ledger.decision_rationale
    assert decision_ledger.evidence_references == [evidence_lineage.lineage_id]
    assert decision_ledger.exception_references == []
    assert decision_ledger.trust_score == trust_record.trust_score
    assert decision_ledger.trust_classification == trust_record.trust_classification
    assert decision_ledger.decision_outcome == trust_record.trust_classification
    assert decision_ledger.decision_timestamp
    assert decision_ledger.created_timestamp

    assert decision_explanation.trust_record_reference == trust_record.trust_record_id
    assert decision_explanation.evidence_count == trust_record.evidence_count
    assert decision_explanation.exception_count == trust_record.exception_count
    assert decision_explanation.exception_penalty == trust_record.exception_penalty
    assert decision_explanation.embargo == trust_record.embargo
    assert decision_explanation.trust_score == trust_record.trust_score
    assert decision_explanation.trust_classification == trust_record.trust_classification
    assert decision_explanation.exception_record_references == []
    assert decision_explanation.decision_path

    required_steps = {
        "EVIDENCE_LINEAGE_CREATED",
        "TRUST_POLICY_SOURCE_LOADED",
        "EXCEPTION_RULES_EVALUATED",
        "TRUST_SCORE_CALCULATED",
        "EXPORT_EMBARGO_EVALUATED",
        "TRUST_CLASSIFICATION_ASSIGNED",
    }
    observed_steps = {step["step"] for step in decision_explanation.decision_path}

    assert required_steps == observed_steps

    outputs_by_step = {
        step["step"]: step["output"]
        for step in decision_explanation.decision_path
    }

    assert outputs_by_step["TRUST_POLICY_SOURCE_LOADED"] == (
        engine.policy.policy_source_metadata()
    )

    assert audit_package.trust_record_reference == trust_record.trust_record_id
    assert audit_package.evidence_lineage_reference == evidence_lineage.lineage_id
    assert audit_package.decision_ledger_reference == decision_ledger.decision_id
    assert audit_package.decision_explanation_reference == (
        decision_explanation.decision_explanation_id
    )
    assert audit_package.rule_version_references == [engine.policy.RULE_VERSION_REFERENCE]
    assert audit_package.exception_references == []
    assert audit_package.export_classification == trust_record.trust_classification


def test_export_embargo_has_no_export_package_but_preserves_audit_chain():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    assert result["export_package"] is None
    assert result["trust_record"].trust_classification == "EXPORT_EMBARGO"
    assert result["audit_package"].export_classification == "EXPORT_EMBARGO"

    audit_package = engine.audit_package_repository.get(
        result["audit_package"].audit_package_id
    )
    trust_record = engine.trust_record_repository.get(
        audit_package.trust_record_reference
    )
    decision_ledger = engine.decision_ledger_repository.get(
        audit_package.decision_ledger_reference
    )
    decision_explanation = engine.decision_explanation_repository.get(
        audit_package.decision_explanation_reference
    )

    assert audit_package == result["audit_package"]
    assert trust_record == result["trust_record"]
    assert decision_ledger == result["decision_ledger"]
    assert decision_explanation == result["decision_explanation"]
    assert audit_package.exception_references == [
        record.exception_id for record in result["exception_records"]
    ]

    outputs_by_step = {
        step["step"]: step["output"]
        for step in decision_explanation.decision_path
    }

    assert outputs_by_step["TRUST_POLICY_SOURCE_LOADED"] == (
        engine.policy.policy_source_metadata()
    )