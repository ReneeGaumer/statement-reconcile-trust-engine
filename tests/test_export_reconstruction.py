from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity
from tests.governance_test_helpers import (
    authorize_engine_rule_version,
    complete_evidence_lineage_metadata,
)


def test_export_package_id_reconstructs_full_authoritative_chain():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

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
        "EVIDENCE_SUFFICIENCY_EVALUATED",
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


def test_broken_export_package_audit_package_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_export_package = engine.export_package_repository.records[
        result["export_package"].export_package_id
    ]
    stored_export_package.audit_package_reference = "MISSING-AUDIT-PACKAGE"

    reconstruction_exception = (
        engine.generate_export_reconstruction_failure_exception(
            result["export_package"].export_package_id
        )
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "export_package.audit_package_reference"
    assert reconstruction_exception.source_reference == result["export_package"].export_package_id
    assert reconstruction_exception.original_value == "MISSING-AUDIT-PACKAGE"
    assert reconstruction_exception.expected_value == "EXISTING_AUTHORITATIVE_RECORD"
    assert "export package" in reconstruction_exception.exception_reason.lower()
    assert "audit package" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_export_embargo_has_no_export_package_but_preserves_audit_chain():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [Severity.CRITICAL],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

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


def test_broken_audit_package_trust_record_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_audit_package = engine.audit_package_repository.records[
        result["audit_package"].audit_package_id
    ]
    stored_audit_package.trust_record_reference = "MISSING-TRUST-RECORD"

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "trust_record_reference"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISSING-TRUST-RECORD"
    assert reconstruction_exception.expected_value == "EXISTING_AUTHORITATIVE_RECORD"
    assert "trust record" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_broken_audit_package_evidence_lineage_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_audit_package = engine.audit_package_repository.records[
        result["audit_package"].audit_package_id
    ]
    stored_audit_package.evidence_lineage_reference = "MISSING-EVIDENCE-LINEAGE"

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "evidence_lineage_reference"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISSING-EVIDENCE-LINEAGE"
    assert reconstruction_exception.expected_value == "EXISTING_AUTHORITATIVE_RECORD"
    assert "evidence lineage" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception

def test_broken_audit_chain_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_audit_package = engine.audit_package_repository.records[
        result["audit_package"].audit_package_id
    ]
    stored_audit_package.decision_ledger_reference = "MISSING-DECISION-LEDGER"

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "decision_ledger_reference"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISSING-DECISION-LEDGER"
    assert reconstruction_exception.expected_value == "EXISTING_AUTHORITATIVE_RECORD"
    assert "decision ledger" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_decision_ledger_trust_record_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_decision_ledger = engine.decision_ledger_repository.records[
        result["decision_ledger"].decision_id
    ]
    stored_decision_ledger.trust_record_reference = "MISMATCHED-TRUST-RECORD"

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "decision_ledger.trust_record_reference"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISMATCHED-TRUST-RECORD"
    assert reconstruction_exception.expected_value == result["audit_package"].trust_record_reference
    assert "decision ledger" in reconstruction_exception.exception_reason.lower()
    assert "trust record" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_decision_ledger_decision_explanation_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_decision_ledger = engine.decision_ledger_repository.records[
        result["decision_ledger"].decision_id
    ]
    stored_decision_ledger.decision_explanation_reference = (
        "MISMATCHED-DECISION-EXPLANATION"
    )

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert (
        reconstruction_exception.field_name
        == "decision_ledger.decision_explanation_reference"
    )
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISMATCHED-DECISION-EXPLANATION"
    assert (
        reconstruction_exception.expected_value
        == result["audit_package"].decision_explanation_reference
    )
    assert "decision ledger" in reconstruction_exception.exception_reason.lower()
    assert "decision explanation" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_audit_package_rule_version_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_audit_package = engine.audit_package_repository.records[
        result["audit_package"].audit_package_id
    ]
    stored_audit_package.rule_version_references = ["MISMATCHED-RULE-VERSION"]

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "audit_package.rule_version_references"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISMATCHED-RULE-VERSION"
    assert reconstruction_exception.expected_value == result["decision_ledger"].rule_version_reference
    assert "rule version" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_decision_explanation_trust_record_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_decision_explanation = engine.decision_explanation_repository.records[
        result["decision_explanation"].decision_explanation_id
    ]
    stored_decision_explanation.trust_record_reference = (
        "MISMATCHED-TRUST-RECORD"
    )

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert (
        reconstruction_exception.field_name
        == "decision_explanation.trust_record_reference"
    )
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISMATCHED-TRUST-RECORD"
    assert (
        reconstruction_exception.expected_value
        == result["audit_package"].trust_record_reference
    )
    assert "decision explanation" in reconstruction_exception.exception_reason.lower()
    assert "trust record" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_decision_ledger_evidence_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_decision_ledger = engine.decision_ledger_repository.records[
        result["decision_ledger"].decision_id
    ]
    stored_decision_ledger.evidence_references = ["MISMATCHED-EVIDENCE-LINEAGE"]

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "decision_ledger.evidence_references"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISMATCHED-EVIDENCE-LINEAGE"
    assert reconstruction_exception.expected_value == result["audit_package"].evidence_lineage_reference
    assert "decision ledger" in reconstruction_exception.exception_reason.lower()
    assert "evidence lineage" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_trust_record_evidence_lineage_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_trust_record = engine.trust_record_repository.records[
        result["trust_record"].trust_record_id
    ]
    stored_trust_record.evidence_lineage_reference = "MISMATCHED-EVIDENCE-LINEAGE"

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "trust_record.evidence_lineage_reference"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MISMATCHED-EVIDENCE-LINEAGE"
    assert reconstruction_exception.expected_value == result["audit_package"].evidence_lineage_reference
    assert "trust record" in reconstruction_exception.exception_reason.lower()
    assert "evidence lineage" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_tampered_decision_explanation_decision_path_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_decision_explanation = engine.decision_explanation_repository.records[
        result["decision_explanation"].decision_explanation_id
    ]
    stored_decision_explanation.decision_path[0]["step"] = "MALICIOUS_STEP"

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "decision_explanation.decision_path"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == "MALICIOUS_STEP"
    assert reconstruction_exception.expected_value == "EVIDENCE_LINEAGE_CREATED"
    assert "decision explanation" in reconstruction_exception.exception_reason.lower()
    assert "decision path" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_mismatched_decision_ledger_exception_references_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [Severity.WARNING],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_decision_ledger = engine.decision_ledger_repository.records[
        result["decision_ledger"].decision_id
    ]
    stored_decision_ledger.exception_references = ["MISMATCHED-EXCEPTION"]

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "decision_ledger.exception_references"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == ["MISMATCHED-EXCEPTION"]
    assert reconstruction_exception.expected_value == result["audit_package"].exception_references
    assert "decision ledger" in reconstruction_exception.exception_reason.lower()
    assert "exception" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception

def test_mismatched_second_audit_package_exception_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [Severity.WARNING, Severity.CRITICAL],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    stored_audit_package = engine.audit_package_repository.records[
        result["audit_package"].audit_package_id
    ]

    original_exception_references = list(stored_audit_package.exception_references)
    assert len(original_exception_references) >= 2

    stored_audit_package.exception_references = [
        original_exception_references[0],
        "MISMATCHED-SECOND-EXCEPTION",
    ]

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "audit_package.exception_references"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == [
        original_exception_references[0],
        "MISMATCHED-SECOND-EXCEPTION",
    ]
    assert reconstruction_exception.expected_value == result[
        "decision_ledger"
    ].exception_references
    assert "audit package" in reconstruction_exception.exception_reason.lower()
    assert "exception" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception


def test_missing_exception_record_reference_generates_reconstruction_failure_exception():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [Severity.WARNING],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    missing_exception_id = result["trust_record"].exception_record_references[0]

    del engine.exception_record_repository.records[missing_exception_id]

    reconstruction_exception = engine.generate_reconstruction_failure_exception(
        result["audit_package"].audit_package_id
    )

    assert reconstruction_exception.rule_name == "AUDIT_PACKAGE_RECONSTRUCTION_REQUIRED"
    assert reconstruction_exception.field_name == "exception_record_reference"
    assert reconstruction_exception.source_reference == result["audit_package"].audit_package_id
    assert reconstruction_exception.original_value == missing_exception_id
    assert reconstruction_exception.expected_value == "EXISTING_EXCEPTION_RECORD"
    assert "exception record" in reconstruction_exception.exception_reason.lower()
    assert "does not exist" in reconstruction_exception.exception_reason.lower()
    assert engine.exception_record_repository.get(
        reconstruction_exception.exception_id
    ) == reconstruction_exception




