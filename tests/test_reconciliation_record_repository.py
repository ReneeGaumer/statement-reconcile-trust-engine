import pytest

from trust_engine.reconciliation.reconciliation_evaluator import ReconciliationEvaluator
from trust_engine.reconciliation.reconciliation_record_repository import (
    ReconciliationRecordRepository,
)


def test_reconciliation_record_repository_saves_and_retrieves_record():
    evaluator = ReconciliationEvaluator()
    repository = ReconciliationRecordRepository()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="1000.00",
        source_reference="statement.pdf",
    )

    repository.save(record)

    assert repository.get(record.reconciliation_id) == record


def test_reconciliation_record_repository_lists_all_records():
    evaluator = ReconciliationEvaluator()
    repository = ReconciliationRecordRepository()

    first_record = evaluator.evaluate(
        field_name="beginning_balance",
        expected_value="900.00",
        actual_value="900.00",
        source_reference="statement.pdf",
    )
    second_record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="999.99",
        source_reference="statement.pdf",
    )

    repository.save(first_record)
    repository.save(second_record)

    assert repository.list_all() == [first_record, second_record]


def test_reconciliation_record_repository_rejects_overwrite():
    evaluator = ReconciliationEvaluator()
    repository = ReconciliationRecordRepository()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="1000.00",
        source_reference="statement.pdf",
    )

    repository.save(record)

    with pytest.raises(ValueError, match="cannot be overwritten"):
        repository.save(record)


def test_reconciliation_record_repository_returns_none_for_missing_record():
    repository = ReconciliationRecordRepository()

    assert repository.get("RECONCILIATION-MISSING") is None