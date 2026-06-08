import pytest

from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory


def test_evidence_lineage_factory():
    factory = EvidenceLineageFactory()
    record = factory.create(
        "statement.pdf",
        source_location="bank-portal",
        page_reference="page-1",
        acquisition_method="UPLOAD",
        evidence_hash="hash-001",
        chain_of_custody=["uploaded-by-user"],
        evidence_type="BANK_STATEMENT",
        evidence_status="CAPTURED",
    )

    assert record.lineage_id
    assert record.lineage_version == "1.0.0"
    assert record.source_document_reference == "statement.pdf"
    assert record.source_location == "bank-portal"
    assert record.page_reference == "page-1"
    assert record.acquisition_method == "UPLOAD"
    assert record.acquisition_timestamp
    assert record.evidence_hash == "hash-001"
    assert record.chain_of_custody == ["uploaded-by-user"]
    assert record.evidence_type == "BANK_STATEMENT"
    assert record.evidence_status == "CAPTURED"
    assert record.created_timestamp


@pytest.mark.parametrize(
    "field_name, kwargs",
    [
        ("source_document_reference", {"source_document_reference": ""}),
        ("source_location", {"source_location": ""}),
        ("page_reference", {"page_reference": ""}),
        ("acquisition_method", {"acquisition_method": ""}),
        ("evidence_hash", {"evidence_hash": ""}),
        ("evidence_type", {"evidence_type": ""}),
        ("evidence_status", {"evidence_status": ""}),
    ],
)
def test_evidence_lineage_factory_rejects_missing_required_fields(field_name, kwargs):
    factory = EvidenceLineageFactory()

    base_kwargs = {
        "source_document_reference": "statement.pdf",
        "source_location": "bank-portal",
        "page_reference": "page-1",
        "acquisition_method": "UPLOAD",
        "evidence_hash": "hash-001",
        "chain_of_custody": ["uploaded-by-user"],
        "evidence_type": "BANK_STATEMENT",
        "evidence_status": "CAPTURED",
    }
    base_kwargs.update(kwargs)

    with pytest.raises(ValueError):
        factory.create(**base_kwargs)