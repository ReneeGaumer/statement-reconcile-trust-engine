from datetime import UTC, datetime

from trust_engine.domain.authoritative_models import CorrectionRecord
from trust_engine.infrastructure.correction_record_repository import (
    CorrectionRecordRepository,
)


def build_correction_record():
    return CorrectionRecord(
        correction_id="CORR-001",
        original_value="100.00",
        corrected_value="100.01",
        correction_reason="Correction repository contract test.",
        correction_timestamp=datetime.now(UTC),
        correction_authorization_reference="GOV-001",
        evidence_reference="EL-001",
        exception_reference="EX-001",
    )


def test_correction_record_repository_stores_authoritative_correction_record():
    record = build_correction_record()
    repo = CorrectionRecordRepository()

    repo.save(record)

    loaded = repo.get("CORR-001")

    assert loaded == record
    assert loaded.original_value == "100.00"
    assert loaded.corrected_value == "100.01"
    assert loaded.correction_authorization_reference == "GOV-001"
    assert loaded.evidence_reference == "EL-001"
    assert loaded.exception_reference == "EX-001"


def test_correction_record_repository_is_append_only():
    record = build_correction_record()
    repo = CorrectionRecordRepository()

    repo.save(record)

    try:
        repo.save(record)
        raise AssertionError("overwrite should have failed")
    except ValueError:
        pass


def test_correction_record_repository_returns_defensive_copies():
    record = build_correction_record()
    repo = CorrectionRecordRepository()

    repo.save(record)

    loaded = repo.get("CORR-001")
    loaded.corrected_value = "999.99"

    loaded_again = repo.get("CORR-001")

    assert loaded_again.corrected_value == "100.01"