from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory


def test_evidence_lineage_factory():
    
    factory = EvidenceLineageFactory()
    record = factory.create("statement.pdf")
    
    assert record.lineage_id
    assert record.source_document_reference == "statement.pdf"
    assert record.acquisition_timestamp
