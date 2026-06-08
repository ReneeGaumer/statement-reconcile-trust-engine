from decimal import Decimal

from trust_engine.reconciliation.reconciliation_evaluator import ReconciliationEvaluator
from trust_engine.reconciliation.reconciliation_status import ReconciliationStatus


def test_reconciliation_evaluator_emits_exact_match_record():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="1000.00",
        source_reference="statement.pdf",
    )

    assert record.status == ReconciliationStatus.MATCH.value
    assert record.variance == Decimal("0.00")
    assert record.rule_reference == "EXACT_AMOUNT_MATCH"


def test_reconciliation_evaluator_emits_tolerance_match_record():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="1000.01",
        tolerance="0.01",
        source_reference="statement.pdf",
    )

    assert record.status == ReconciliationStatus.MATCH_WITH_TOLERANCE.value
    assert record.variance == Decimal("0.01")
    assert record.tolerance == Decimal("0.01")
    assert record.rule_reference == "TOLERANCE_AMOUNT_MATCH"


def test_reconciliation_evaluator_emits_mismatch_record():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="999.98",
        tolerance="0.01",
        source_reference="statement.pdf",
    )

    assert record.status == ReconciliationStatus.MISMATCH.value
    assert record.variance == Decimal("-0.02")
    assert record.rule_reference == "EXACT_AMOUNT_MATCH"


def test_reconciliation_evaluator_emits_missing_expected_record():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value=None,
        actual_value="1000.00",
        source_reference="statement.pdf",
    )

    assert record.status == ReconciliationStatus.MISSING_EXPECTED.value
    assert record.variance is None
    assert record.rule_reference == "MISSING_EXPECTED_VALUE"


def test_reconciliation_evaluator_emits_missing_actual_record():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value=None,
        source_reference="statement.pdf",
    )

    assert record.status == ReconciliationStatus.MISSING_ACTUAL.value
    assert record.variance is None
    assert record.rule_reference == "MISSING_ACTUAL_VALUE"


def test_reconciliation_evaluator_emits_unreconcilable_record_for_non_numeric_values():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="not-a-number",
        actual_value="1000.00",
        source_reference="statement.pdf",
    )

    assert record.status == ReconciliationStatus.UNRECONCILABLE.value
    assert record.variance is None
    assert record.rule_reference == "UNRECONCILABLE_VALUE_COMPARISON"


def test_reconciliation_evaluator_preserves_original_values_without_correction():
    evaluator = ReconciliationEvaluator()

    record = evaluator.evaluate(
        field_name="ending_balance",
        expected_value="$1,000.00",
        actual_value="1000.00",
        source_reference="statement.pdf",
    )

    assert record.expected_value == "$1,000.00"
    assert record.actual_value == "1000.00"
    assert record.status == ReconciliationStatus.UNRECONCILABLE.value