from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.severity import Severity


def test_trust_model_policy_defines_current_runtime_penalties():
    policy = TrustModelPolicy()

    assert policy.penalty_for(Severity.INFO) == 0.0
    assert policy.penalty_for(Severity.WARNING) == 5.0
    assert policy.penalty_for(Severity.HIGH) == 20.0
    assert policy.penalty_for(Severity.CRITICAL) == 50.0


def test_trust_model_policy_defines_current_runtime_classifications():
    policy = TrustModelPolicy()

    assert policy.classify(100.0, False) == "CLEAN_EXPORT"
    assert policy.classify(90.0, False) == "CLEAN_EXPORT"
    assert policy.classify(89.99, False) == "EXPORT_WITH_WARNINGS"
    assert policy.classify(75.0, False) == "EXPORT_WITH_WARNINGS"
    assert policy.classify(74.99, False) == "PARTIAL_EXPORT"
    assert policy.classify(50.0, False) == "PARTIAL_EXPORT"
    assert policy.classify(49.99, False) == "UNSAFE_EXPORT"


def test_trust_model_policy_embargo_overrides_score():
    policy = TrustModelPolicy()

    assert policy.classify(100.0, True) == "EXPORT_EMBARGO"


def test_trust_model_policy_embargo_rule_uses_critical_severity():
    policy = TrustModelPolicy()

    assert policy.should_embargo([Severity.WARNING]) is False
    assert policy.should_embargo([Severity.CRITICAL]) is True