import json

import pytest

from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.severity import Severity


def write_policy_files(directory, impact_rules=None, threshold_rules=None):
    impact_rules = impact_rules or {
        "INFO": -5,
        "WARNING": -15,
        "HIGH": -40,
        "CRITICAL": -100,
    }
    threshold_rules = threshold_rules or {
        "100": "CLEAN_EXPORT",
        "85-99": "EXPORT_WITH_WARNINGS",
        "60-84": "PARTIAL_EXPORT",
        "1-59": "UNSAFE_EXPORT",
    }

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "trust-impact-rules.schema.json").write_text(
        json.dumps(impact_rules),
        encoding="utf-8",
    )
    (directory / "trust-classification-thresholds.schema.json").write_text(
        json.dumps(threshold_rules),
        encoding="utf-8",
    )


def test_trust_model_policy_can_load_from_explicit_directory(tmp_path):
    policy_dir = tmp_path / "policy"
    write_policy_files(
        policy_dir,
        impact_rules={
            "INFO": -1,
            "WARNING": -2,
            "HIGH": -3,
            "CRITICAL": -4,
        },
        threshold_rules={
            "100": "CLEAN_EXPORT",
            "85-99": "EXPORT_WITH_WARNINGS",
            "60-84": "PARTIAL_EXPORT",
            "1-59": "UNSAFE_EXPORT",
        },
    )

    policy = TrustModelPolicy(policy_dir)

    assert policy.penalty_for(Severity.INFO) == 1.0
    assert policy.penalty_for(Severity.WARNING) == 2.0
    assert policy.penalty_for(Severity.HIGH) == 3.0
    assert policy.penalty_for(Severity.CRITICAL) == 4.0


def test_trust_model_policy_fails_clearly_when_policy_file_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="Trust model policy file not found"):
        TrustModelPolicy(tmp_path / "missing-policy")


def test_trust_model_policy_fails_clearly_when_impact_key_missing(tmp_path):
    policy_dir = tmp_path / "policy"
    write_policy_files(
        policy_dir,
        impact_rules={
            "INFO": -5,
            "WARNING": -15,
            "HIGH": -40,
        },
    )

    with pytest.raises(KeyError, match="missing required keys"):
        TrustModelPolicy(policy_dir)


def test_trust_model_policy_fails_clearly_when_threshold_key_missing(tmp_path):
    policy_dir = tmp_path / "policy"
    write_policy_files(
        policy_dir,
        threshold_rules={
            "100": "CLEAN_EXPORT",
            "85-99": "EXPORT_WITH_WARNINGS",
            "60-84": "PARTIAL_EXPORT",
        },
    )

    with pytest.raises(KeyError, match="missing required keys"):
        TrustModelPolicy(policy_dir)