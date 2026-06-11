from trust_engine.application.trust_engine import TrustEngine
from tests.governance_test_helpers import (
    authorize_engine_rule_version,
    complete_evidence_lineage_metadata,
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


def test_trust_engine_rejects_missing_governance_with_authority_diagnostics():
    engine = TrustEngine()

    try:
        engine.determine_trust(10, [], "statement.pdf")
        raise AssertionError("unauthorized governance should stop trust execution")
    except PermissionError as error:
        message = str(error)

    assert engine.policy.RULE_VERSION_REFERENCE in message
    assert "MISSING_RULE_VERSION" in message


def test_trust_engine_allows_export_when_rule_version_is_authorized():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"
    assert result["decision_ledger"].rule_version_reference == (
        engine.policy.RULE_VERSION_REFERENCE
    )
    assert result["audit_package"].rule_version_references == [
        engine.policy.RULE_VERSION_REFERENCE
    ]
    assert result["export_package"] is not None