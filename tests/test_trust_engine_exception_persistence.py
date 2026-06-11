from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity
from tests.governance_test_helpers import authorize_engine_rule_version


def test_trust_engine_exception_persistence():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10, [Severity.WARNING, Severity.CRITICAL], "statement.pdf"
    )

    exceptions = result["exception_records"]
    severity_exceptions = [
        record for record in exceptions if record.field_name == "TRUST_SEVERITY"
    ]

    assert len(severity_exceptions) == 2
    assert severity_exceptions[0].severity == "WARNING"
    assert severity_exceptions[0].penalty == 15.0
    assert severity_exceptions[0].source_reference == "statement.pdf"
    assert severity_exceptions[0].field_name == "TRUST_SEVERITY"
    assert severity_exceptions[0].original_value == "WARNING"
    assert severity_exceptions[0].expected_value == "NO_EXCEPTION"
    assert severity_exceptions[1].severity == "CRITICAL"
    assert severity_exceptions[1].penalty == 100.0

    assert result["exception_penalty"] == sum(
        record.penalty for record in exceptions
    )

    stored = engine.exception_record_repository.all()
    assert len(stored) == len(exceptions)
    assert [record.exception_id for record in stored] == [
        record.exception_id for record in exceptions
    ]