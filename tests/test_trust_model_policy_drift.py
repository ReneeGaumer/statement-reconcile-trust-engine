import json
from pathlib import Path

from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.severity import Severity


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_runtime_policy_aligns_with_trust_impact_rules():
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

    assert runtime_penalties == documented_penalties


def test_runtime_policy_aligns_with_threshold_rules():
    policy = TrustModelPolicy()
    threshold_rules = load_json(
        "trust-model/classifications/trust-classification-thresholds.schema.json"
    )

    assert threshold_rules["100"] == "CLEAN_EXPORT"
    assert threshold_rules["85-99"] == "EXPORT_WITH_WARNINGS"
    assert threshold_rules["60-84"] == "PARTIAL_EXPORT"
    assert threshold_rules["1-59"] == "UNSAFE_EXPORT"

    assert policy.classify(100.0, False) == threshold_rules["100"]
    assert policy.classify(99.99, False) == threshold_rules["85-99"]
    assert policy.classify(85.0, False) == threshold_rules["85-99"]
    assert policy.classify(84.99, False) == threshold_rules["60-84"]
    assert policy.classify(60.0, False) == threshold_rules["60-84"]
    assert policy.classify(59.99, False) == threshold_rules["1-59"]
    assert policy.classify(1.0, False) == threshold_rules["1-59"]