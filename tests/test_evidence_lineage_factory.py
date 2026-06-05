from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory

factory = EvidenceLineageFactory()
record = factory.create("statement.pdf")

print(record)
assert record.lineage_id
assert record.source_document_reference == "statement.pdf"
assert record.acquisition_timestamp
print("PASS")
