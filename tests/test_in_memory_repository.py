import pytest

from trust_engine.infrastructure.in_memory_repository import InMemoryRepository


def test_in_memory_repository():
    repo = InMemoryRepository()

    record = {
        "trust_record_id": "TR-001",
        "trust_score": 100.0,
    }

    saved = repo.save("TR-001", record)
    loaded = repo.get("TR-001")

    assert saved == record
    assert loaded == record
    assert repo.all() == [record]


def test_in_memory_repository_rejects_duplicate_ids():
    repo = InMemoryRepository()

    repo.save("id1", "record")

    with pytest.raises(ValueError):
        repo.save("id1", "other")