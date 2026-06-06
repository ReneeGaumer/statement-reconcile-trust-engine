from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity


def test_export_package_id_reconstructs_full_authoritative_chain():
    engine = TrustEngine()
    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    export_package_id = result["export_package"].export_package_id
    del result

    export = engine.export_package_repository.get(export_package_id)
    audit = engine.audit_package_repository.get(export.audit_package_reference)
    trust_record = engine.trust_record_repository.get(audit.trust_record_reference)
    decision_explanation = engine.decision_explanation_repository.get(audit.decision_explanation_reference)
    exception_records = [
        engine.exception_record_repository.get(exception_id)
        for exception_id in decision_explanation.exception_record_references
    ]
    lineage = engine.evidence_lineage_repository.get(audit.evidence_lineage_reference)

    assert export.export_package_id == export_package_id
    assert export.audit_package_reference == audit.audit_package_id
    assert export.trust_record_reference == trust_record.trust_record_id
    assert audit.trust_record_reference == trust_record.trust_record_id
    assert audit.decision_explanation_reference == decision_explanation.decision_explanation_id
    assert audit.evidence_lineage_reference == lineage.lineage_id
    assert trust_record.evidence_lineage_reference == lineage.lineage_id
    assert trust_record.exception_record_references == [exception.exception_id for exception in exception_records]
    assert decision_explanation.trust_record_reference == trust_record.trust_record_id
    assert decision_explanation.exception_record_references == [exception.exception_id for exception in exception_records]
    assert len(exception_records) == 1
    assert exception_records[0].exception_id in trust_record.exception_record_references
    assert lineage.source_document_reference == "statement.pdf"
    assert trust_record.trust_classification == "EXPORT_EMBARGO"
    assert export.export_classification == trust_record.trust_classification
