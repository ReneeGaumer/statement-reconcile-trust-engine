from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity


def test_trust_engine_end_to_end_clean_export():
    engine = TrustEngine()
    clean = engine.determine_trust(10, [], "statement.pdf")
    lineage = clean["evidence_lineage"]
    record = clean["trust_record"]
    ledger = clean["decision_ledger"]
    explanation = clean["decision_explanation"]

    assert lineage.lineage_id
    assert lineage.source_document_reference == "statement.pdf"
    assert record.trust_score == 100.0
    assert record.trust_classification == "CLEAN_EXPORT"
    assert clean["embargo"] is False
    assert ledger.trust_record_reference == record.trust_record_id
    assert explanation.trust_record_reference == record.trust_record_id
    assert record.evidence_lineage_reference == lineage.lineage_id
    assert record.exception_record_references == []


def test_trust_engine_end_to_end_export_embargo():
    engine = TrustEngine()
    embargoed = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")
    embargo_lineage = embargoed["evidence_lineage"]
    embargo_record = embargoed["trust_record"]
    embargo_ledger = embargoed["decision_ledger"]
    embargo_explanation = embargoed["decision_explanation"]

    assert embargo_lineage.source_document_reference == "statement.pdf"
    assert embargo_record.trust_classification == "EXPORT_EMBARGO"
    assert embargoed["embargo"] is True
    assert embargoed["exception_penalty"] == 100.0
    assert embargo_ledger.trust_record_reference == embargo_record.trust_record_id
    assert embargo_explanation.embargo is True
    assert embargo_record.evidence_lineage_reference == embargo_lineage.lineage_id
    assert embargo_record.exception_record_references == [embargoed["exception_records"][0].exception_id]
