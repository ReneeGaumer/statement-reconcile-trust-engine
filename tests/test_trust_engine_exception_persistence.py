from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity


def test_trust_engine_exception_persistence():
    engine = TrustEngine()
    result = engine.determine_trust(10, [Severity.WARNING, Severity.CRITICAL], "statement.pdf")

    exceptions = result["exception_records"]

    assert len(exceptions) == 2
    assert result["exception_penalty"] == 115.0
    assert exceptions[0].severity == "WARNING"
    assert exceptions[0].penalty == 15.0
    assert exceptions[0].source_reference == "statement.pdf"
    assert exceptions[0].field_name == "TRUST_SEVERITY"
    assert exceptions[0].original_value == "WARNING"
    assert exceptions[0].expected_value == "NO_EXCEPTION"
    assert exceptions[1].severity == "CRITICAL"
    assert exceptions[1].penalty == 100.0

    stored = engine.exception_record_repository.all()
    assert len(stored) == 2
    assert [record.exception_id for record in stored] == [
        record.exception_id for record in exceptions
    ]