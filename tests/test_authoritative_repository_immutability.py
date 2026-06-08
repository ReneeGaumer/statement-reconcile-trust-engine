import pytest

from trust_engine.application.trust_record_factory import TrustRecordFactory
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository


def test_authoritative_repository_saved_record_cannot_be_mutated_through_original_reference():
    repo = TrustRecordRepository()
    record = TrustRecordFactory().create(100.0, "CLEAN_EXPORT")

    repo.save(record)

    record.trust_score = 0.0
    record.trust_classification = "EXPORT_EMBARGO"

    loaded = repo.get(record.trust_record_id)

    assert loaded.trust_score == 100.0
    assert loaded.trust_classification == "CLEAN_EXPORT"


def test_authoritative_repository_returned_record_cannot_mutate_stored_record():
    repo = TrustRecordRepository()
    record = TrustRecordFactory().create(100.0, "CLEAN_EXPORT")

    repo.save(record)

    loaded = repo.get(record.trust_record_id)
    loaded.trust_score = 0.0
    loaded.trust_classification = "EXPORT_EMBARGO"

    loaded_again = repo.get(record.trust_record_id)

    assert loaded_again.trust_score == 100.0
    assert loaded_again.trust_classification == "CLEAN_EXPORT"
