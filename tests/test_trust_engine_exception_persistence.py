from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity

engine = TrustEngine()
result = engine.determine_trust(10, [Severity.WARNING, Severity.CRITICAL], "statement.pdf")
exceptions = result["exception_records"]

print(exceptions)
assert len(exceptions) == 2
assert result["exception_penalty"] == 55.0
assert result["trust_record"].trust_classification == "EXPORT_EMBARGO"
assert len(engine.exception_record_repository.all()) == 2

for exception in exceptions:
    loaded = engine.exception_record_repository.get(exception.exception_id)
    assert loaded == exception
    assert exception.rule_name.endswith("_EXCEPTION_RULE")

print("PASS")
