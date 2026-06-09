from datetime import datetime

from trust_engine.application.correction_record_factory import CorrectionRecordFactory


def test_correction_record_factory_creates_complete_correction_record():
    record = CorrectionRecordFactory().create(
        original_value="100.00",
        corrected_value="100.01",
        correction_reason="Authorized correction after evidence review.",
        correction_authorization_reference="GOV-001",
        evidence_reference="EL-001",
        exception_reference="EX-001",
    )

    assert record.correction_id.startswith("CORR-")
    assert record.original_value == "100.00"
    assert record.corrected_value == "100.01"
    assert record.correction_reason == "Authorized correction after evidence review."
    assert isinstance(record.correction_timestamp, datetime)
    assert record.correction_authorization_reference == "GOV-001"
    assert record.evidence_reference == "EL-001"
    assert record.exception_reference == "EX-001"