from dataclasses import FrozenInstanceError

import pytest

from trust_engine.reconciliation.reconciliation_record import ReconciliationRecord
from trust_engine.reconciliation.reconciliation_status import ReconciliationStatus


def test_reconciliation_record_captures_comparison_evidence():
    record = ReconciliationRecord.create(
        field_name="ending_balance",
        expected_value=1000.00,
        actual_value=1000.00,
        variance=0.00,
        tolerance=0.00,
        status=ReconciliationStatus.MATCH.value,
        source_reference="statement.pdf",
        rule_reference="EXACT_AMOUNT_MATCH",
    )

    assert record.reconciliation_id.startswith("RECONCILIATION-")
    assert record.field_name == "ending_balance"
    assert record.expected_value == 1000.00
    assert record.actual_value == 1000.00
    assert record.variance == 0.00
    assert record.tolerance == 0.00
    assert record.status == "MATCH"
    assert record.source_reference == "statement.pdf"
    assert record.rule_reference == "EXACT_AMOUNT_MATCH"
    assert record.created_timestamp


def test_reconciliation_record_is_immutable():
    record = ReconciliationRecord.create(
        field_name="ending_balance",
        expected_value=1000.00,
        actual_value=999.99,
        variance=-0.01,
        tolerance=0.00,
        status=ReconciliationStatus.MISMATCH.value,
        source_reference="statement.pdf",
        rule_reference="EXACT_AMOUNT_MATCH",
    )

    with pytest.raises(FrozenInstanceError):
        record.actual_value = 1000.00


def test_reconciliation_status_defines_trust_safe_outcomes():
    assert ReconciliationStatus.MATCH.value == "MATCH"
    assert ReconciliationStatus.MATCH_WITH_TOLERANCE.value == "MATCH_WITH_TOLERANCE"
    assert ReconciliationStatus.MISMATCH.value == "MISMATCH"
    assert ReconciliationStatus.MISSING_EXPECTED.value == "MISSING_EXPECTED"
    assert ReconciliationStatus.MISSING_ACTUAL.value == "MISSING_ACTUAL"
    assert ReconciliationStatus.UNRECONCILABLE.value == "UNRECONCILABLE"