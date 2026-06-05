from trust_engine.application.exception_record_factory import ExceptionRecordFactory
from trust_engine.infrastructure.exception_record_repository import ExceptionRecordRepository

factory = ExceptionRecordFactory()
repo = ExceptionRecordRepository()
record = factory.create("CRITICAL", 50.0, "CRITICAL_EXCEPTION_EMBARGO_RULE")

saved = repo.save(record)
loaded = repo.get(record.exception_id)

print(saved)
assert loaded == record
assert record.severity == "CRITICAL"
assert record.penalty == 50.0
assert record.rule_name == "CRITICAL_EXCEPTION_EMBARGO_RULE"

try:
    repo.save(record)
    raise AssertionError("Overwrite should have failed")
except ValueError:
    print("Immutable save protection confirmed")

print("PASS")
