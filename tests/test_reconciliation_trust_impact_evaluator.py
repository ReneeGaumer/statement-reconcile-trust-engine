from trust_engine.application.reconciliation_trust_impact_evaluator import (
    ReconciliationTrustImpactEvaluator,
)
from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.reconciliation.reconciliation_evaluator import ReconciliationEvaluator


def test_reconciliation_trust_impact_evaluator_returns_policy_severity_for_impact_status():
    policy = TrustModelPolicy()
    evaluator = ReconciliationTrustImpactEvaluator(policy)
    reconciliation_evaluator = ReconciliationEvaluator()

    reconciliation_record = reconciliation_evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="900.00",
        tolerance=0,
        source_reference="statement.pdf",
    )

    severities = evaluator.severities_for([reconciliation_record])

    assert severities == [policy.reconciliation_trust_impact_severity()]


def test_reconciliation_trust_impact_evaluator_returns_no_severity_for_clean_match():
    policy = TrustModelPolicy()
    evaluator = ReconciliationTrustImpactEvaluator(policy)
    reconciliation_evaluator = ReconciliationEvaluator()

    reconciliation_record = reconciliation_evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="1000.00",
        tolerance=0,
        source_reference="statement.pdf",
    )

    assert evaluator.severities_for([reconciliation_record]) == []


def test_reconciliation_trust_impact_evaluator_preserves_input_order():
    policy = TrustModelPolicy()
    evaluator = ReconciliationTrustImpactEvaluator(policy)
    reconciliation_evaluator = ReconciliationEvaluator()

    mismatch = reconciliation_evaluator.evaluate(
        field_name="ending_balance",
        expected_value="1000.00",
        actual_value="900.00",
        tolerance=0,
        source_reference="statement.pdf",
    )
    match = reconciliation_evaluator.evaluate(
        field_name="beginning_balance",
        expected_value="500.00",
        actual_value="500.00",
        tolerance=0,
        source_reference="statement.pdf",
    )
    missing_actual = reconciliation_evaluator.evaluate(
        field_name="interest",
        expected_value="10.00",
        actual_value=None,
        tolerance=0,
        source_reference="statement.pdf",
    )

    severities = evaluator.severities_for([mismatch, match, missing_actual])

    assert severities == [
        policy.reconciliation_trust_impact_severity(),
        policy.reconciliation_trust_impact_severity(),
    ]