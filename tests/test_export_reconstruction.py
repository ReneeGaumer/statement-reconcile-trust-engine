from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity


def test_export_package_id_reconstructs_full_authoritative_chain():
    engine = TrustEngine()
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


def test_export_embargo_has_no_export_package_but_preserves_audit_chain():
    engine = TrustEngine()
    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    audit_package = result["audit_package"]
    trust_record = result["trust_record"]
    decision_ledger = result["decision_ledger"]
    evidence_lineage = result["evidence_lineage"]

    assert result["embargo"] is True
    assert result["export_package"] is None
    assert trust_record.trust_classification == "EXPORT_EMBARGO"

    assert engine.audit_package_repository.get(audit_package.audit_package_id) == audit_package
    assert engine.trust_record_repository.get(trust_record.trust_record_id) == trust_record
    assert engine.decision_ledger_repository.get(decision_ledger.decision_id) == decision_ledger
    assert engine.evidence_lineage_repository.get(evidence_lineage.lineage_id) == evidence_lineage