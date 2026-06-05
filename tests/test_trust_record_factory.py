from trust_engine.application.trust_record_factory import TrustRecordFactory


def test_trust_record_factory():
    
    factory = TrustRecordFactory()
    record = factory.create(100.0, "CLEAN_EXPORT")
    
    assert record.trust_score == 100.0
    assert record.trust_classification == "CLEAN_EXPORT"
    assert record.trust_record_id
    assert record.created_timestamp
