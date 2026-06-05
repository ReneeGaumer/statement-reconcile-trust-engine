from trust_engine.infrastructure.in_memory_repository import InMemoryRepository

repo = InMemoryRepository()
record = {"trust_record_id": "TR-001", "trust_score": 100.0}

saved = repo.save("TR-001", record)
loaded = repo.get("TR-001")

print(saved)
print(loaded)

assert loaded == record

try:
    repo.save("TR-001", record)
    raise AssertionError("Overwrite should have failed")
except ValueError:
    print("Immutable save protection confirmed")

print("PASS")
