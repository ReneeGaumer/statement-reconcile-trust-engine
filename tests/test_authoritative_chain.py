from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity


def test_authoritative_chain_export_embargo():
    engine = TrustEngine()
    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    lineage = result["evidence_lineage"]
    exceptions = result["exception_records"]
    trust_record = result["trust_record"]
    ledger = result["decision_ledger"]
    audit = result["audit_package"]
    export = result["export_package"]

    assert len(exceptions) == 1
    assert engine.exception_record_repository.get(exceptions[0].exception_id) == exceptions[0]
    assert engine.evidence_lineage_repository.get(lineage.lineage_id) == lineage
    assert engine.trust_record_repository.get(trust_record.trust_record_id) == trust_record
    assert engine.decision_ledger_repository.get(ledger.decision_id) == ledger
    assert engine.audit_package_repository.get(audit.audit_package_id) == audit
    assert engine.export_package_repository.get(export.export_package_id) == export

    assert ledger.trust_record_reference == trust_record.trust_record_id
    assert ledger.decision_explanation_reference == result["decision_explanation"].decision_explanation_id
    assert audit.trust_record_reference == trust_record.trust_record_id
    assert audit.evidence_lineage_reference == lineage.lineage_id
    assert audit.decision_ledger_reference == ledger.decision_id
    assert audit.decision_explanation_reference == result["decision_explanation"].decision_explanation_id
    assert export.trust_record_reference == trust_record.trust_record_id
    assert export.audit_package_reference == audit.audit_package_id
    assert export.export_classification == "EXPORT_EMBARGO"
    assert trust_record.trust_classification == "EXPORT_EMBARGO"
    assert trust_record.evidence_lineage_reference == lineage.lineage_id
    assert trust_record.exception_record_references == [exceptions[0].exception_id]

    explanation = result["decision_explanation"]
    assert engine.decision_explanation_repository.get(explanation.decision_explanation_id) == explanation
    assert explanation.trust_record_reference == trust_record.trust_record_id
    assert explanation.exception_record_references == [exceptions[0].exception_id]
    assert explanation.decision_path[-1]["output"] == trust_record.trust_classification
