import json
from pathlib import Path

from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.severity import Severity


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_runtime_policy_drift_from_trust_impact_rules_is_explicit():
    policy = TrustModelPolicy()
    trust_impact_rules = load_json(
        "trust-model/classifications/trust-impact-rules.schema.json"
    )

    documented_penalties = {
        Severity.INFO: abs(float(trust_impact_rules["INFO"])),
        Severity.WARNING: abs(float(trust_impact_rules["WARNING"])),
        Severity.HIGH: abs(float(trust_impact_rules["HIGH"])),
        Severity.CRITICAL: abs(float(trust_impact_rules["CRITICAL"])),
    }

    runtime_penalties = {
        Severity.INFO: policy.penalty_for(Severity.INFO),
        Severity.WARNING: policy.penalty_for(Severity.WARNING),
        Severity.HIGH: policy.penalty_for(Severity.HIGH),
        Severity.CRITICAL: policy.penalty_for(Severity.CRITICAL),
    }

    assert runtime_penalties != documented_penalties
    assert documented_penalties == {
        Severity.INFO: 5.0,
        Severity.WARNING: 15.0,
        Severity.HIGH: 40.0,
        Severity.CRITICAL: 100.0,
    }
    assert runtime_penalties == {
        Severity.INFO: 0.0,
        Severity.WARNING: 5.0,
        Severity.HIGH: 20.0,
        Severity.CRITICAL: 50.0,
    }


def test_runtime_policy_drift_from_threshold_rules_is_explicit():
    policy = TrustModelPolicy()
    threshold_rules = load_json(
        "trust-model/classifications/trust-classification-thresholds.schema.json"
    )

    assert threshold_rules["85-99"] == "EXPORT_WITH_WARNINGS"
    assert threshold_rules["60-84"] == "PARTIAL_EXPORT"
    assert threshold_rules["1-59"] == "UNSAFE_EXPORT"

    assert policy.classify(85.0, False) == "EXPORT_WITH_WARNINGS"
    assert policy.classify(60.0, False) == "PARTIAL_EXPORT"

    assert policy.classify(84.99, False) == "EXPORT_WITH_WARNINGS"
    assert policy.classify(59.99, False) == "PARTIAL_EXPORT"