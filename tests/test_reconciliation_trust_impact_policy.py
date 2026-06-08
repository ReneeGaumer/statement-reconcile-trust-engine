from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.reconciliation.reconciliation_status import ReconciliationStatus


def test_reconciliation_statuses_that_trigger_trust_impact_are_policy_defined():
    policy = TrustModelPolicy()

    assert policy.reconciliation_trust_impact_statuses() == {
        ReconciliationStatus.MISMATCH.value,
        ReconciliationStatus.MISSING_EXPECTED.value,
        ReconciliationStatus.MISSING_ACTUAL.value,
        ReconciliationStatus.UNRECONCILABLE.value,
    }


def test_reconciliation_trust_impact_severity_is_policy_defined():
    policy = TrustModelPolicy()

    assert policy.reconciliation_trust_impact_severity().value == "WARNING"