import pytest

from trust_engine.application.decision_explanation_factory import DecisionExplanationFactory


VALID_DECISION_PATH = [
    {
        "step": "TRUST_SCORE_CALCULATED",
        "rule": "EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY",
        "inputs": {"evidence_count": 10, "exception_penalty": 50.0},
        "output": 50.0,
    },
    {
        "step": "EXPORT_EMBARGO_EVALUATED",
        "rule": "CRITICAL_SEVERITY_TRIGGERS_EXPORT_EMBARGO",
        "inputs": {"severities": ["CRITICAL"]},
        "output": True,
    },
]


def valid_kwargs():
    return {
        "trust_record_reference": "TR-001",
        "evidence_count": 10,
        "exception_count": 1,
        "exception_penalty": 50.0,
        "embargo": True,
        "trust_score": 50.0,
        "trust_classification": "EXPORT_EMBARGO",
        "decision_path": VALID_DECISION_PATH,
        "exception_record_references": ["EX-001"],
    }


def test_decision_explanation_factory():
    factory = DecisionExplanationFactory()
    record = factory.create(**valid_kwargs())

    assert record.decision_explanation_id
    assert record.trust_record_reference == "TR-001"
    assert record.exception_record_references == ["EX-001"]
    assert record.evidence_count == 10
    assert record.exception_count == 1
    assert record.exception_penalty == 50.0
    assert record.embargo is True
    assert record.trust_score == 50.0
    assert record.trust_classification == "EXPORT_EMBARGO"
    assert record.decision_path == VALID_DECISION_PATH
    assert record.created_timestamp


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("trust_record_reference", ""),
        ("evidence_count", None),
        ("exception_count", None),
        ("exception_penalty", None),
        ("embargo", None),
        ("trust_score", None),
        ("trust_classification", ""),
        ("decision_path", []),
    ],
)
def test_decision_explanation_factory_rejects_missing_required_fields(field_name, value):
    factory = DecisionExplanationFactory()
    kwargs = valid_kwargs()
    kwargs[field_name] = value

    with pytest.raises(ValueError):
        factory.create(**kwargs)


@pytest.mark.parametrize(
    "bad_step",
    [
        {"rule": "RULE", "inputs": {}, "output": "OUT"},
        {"step": "STEP", "inputs": {}, "output": "OUT"},
        {"step": "STEP", "rule": "RULE", "output": "OUT"},
        {"step": "STEP", "rule": "RULE", "inputs": {}},
    ],
)
def test_decision_explanation_factory_rejects_incomplete_decision_path_steps(bad_step):
    factory = DecisionExplanationFactory()
    kwargs = valid_kwargs()
    kwargs["decision_path"] = [bad_step]

    with pytest.raises(ValueError):
        factory.create(**kwargs)