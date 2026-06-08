import pytest

from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory


def test_decision_ledger_factory():
    factory = DecisionLedgerFactory()
    entry = factory.create(
        trust_record_reference="TR-001",
        decision_explanation_reference="DE-001",
        rule_version_reference="TRUST_MODEL_RULES_V1",
        decision_rationale="Trust classification derived from evidence and exceptions.",
        evidence_references=["EL-001"],
        exception_references=["EX-001"],
        trust_score=75.0,
        trust_classification="EXPORT_WITH_WARNINGS",
        decision_outcome="EXPORT_WITH_WARNINGS",
    )

    assert entry.decision_id
    assert entry.trust_record_reference == "TR-001"
    assert entry.decision_explanation_reference == "DE-001"
    assert entry.rule_version_reference == "TRUST_MODEL_RULES_V1"
    assert entry.decision_rationale == "Trust classification derived from evidence and exceptions."
    assert entry.evidence_references == ["EL-001"]
    assert entry.exception_references == ["EX-001"]
    assert entry.trust_score == 75.0
    assert entry.trust_classification == "EXPORT_WITH_WARNINGS"
    assert entry.decision_outcome == "EXPORT_WITH_WARNINGS"
    assert entry.decision_timestamp
    assert entry.created_timestamp


@pytest.mark.parametrize(
    "field_name, kwargs",
    [
        ("decision_rationale", {"decision_rationale": ""}),
        ("evidence_references", {"evidence_references": None}),
        ("exception_references", {"exception_references": None}),
        ("trust_score", {"trust_score": None}),
        ("trust_classification", {"trust_classification": ""}),
        ("decision_outcome", {"decision_outcome": ""}),
    ],
)
def test_decision_ledger_factory_rejects_missing_required_fields(field_name, kwargs):
    factory = DecisionLedgerFactory()

    base_kwargs = {
        "trust_record_reference": "TR-001",
        "decision_explanation_reference": "DE-001",
        "rule_version_reference": "TRUST_MODEL_RULES_V1",
        "decision_rationale": "Trust classification derived from evidence and exceptions.",
        "evidence_references": ["EL-001"],
        "exception_references": ["EX-001"],
        "trust_score": 75.0,
        "trust_classification": "EXPORT_WITH_WARNINGS",
        "decision_outcome": "EXPORT_WITH_WARNINGS",
    }
    base_kwargs.update(kwargs)

    with pytest.raises(ValueError):
        factory.create(**base_kwargs)