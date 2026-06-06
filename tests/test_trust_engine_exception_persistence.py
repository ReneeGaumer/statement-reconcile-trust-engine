from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity

def test_trust_engine_exception_persistence():
    engine = TrustEngine()
    result = engine.determine_trust(10, [Severity.WARNING, Severity.CRITICAL], "statement.pdf")

    exceptions = result["exception_records"]

    assert len(exceptions) == 2
    assert result["exception_penalty"] == 55.0
    assert result["trust_record"].trust_classification == "EXPORT_EMBARGO"
    assert len(engine.exception_record_repository.all()) == 2

    for exception in exceptions:
        loaded = engine.exception_record_repository.get(exception.exception_id)
        assert loaded == exception
        assert exception.rule_name.endswith("_EXCEPTION_RULE")
        assert exception.source_reference == "statement.pdf"
        assert exception.field_name == "TRUST_SEVERITY"
        assert exception.expected_value == "NO_EXCEPTION"
        assert "triggered trust exception" in exception.exception_reason
        assert exception.original_value in ["WARNING", "CRITICAL"]
