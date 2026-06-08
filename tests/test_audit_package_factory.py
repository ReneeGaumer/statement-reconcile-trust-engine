import pytest

from trust_engine.application.audit_package_factory import AuditPackageFactory


def test_audit_package_factory():
    factory = AuditPackageFactory()
    package = factory.create(
        trust_record_reference="TR-001",
        evidence_lineage_reference="EL-001",
        decision_ledger_reference="DL-001",
        decision_explanation_reference="DE-001",
        rule_version_references=["TRUST_MODEL_RULES_V1"],
        exception_references=["EX-001"],
        trust_score=85.0,
        trust_classification="EXPORT_WITH_WARNINGS",
        export_classification="EXPORT_WITH_WARNINGS",
    )

    assert package.audit_package_id
    assert package.trust_record_reference == "TR-001"
    assert package.evidence_lineage_reference == "EL-001"
    assert package.decision_ledger_reference == "DL-001"
    assert package.decision_explanation_reference == "DE-001"
    assert package.rule_version_references == ["TRUST_MODEL_RULES_V1"]
    assert package.exception_references == ["EX-001"]
    assert package.trust_score == 85.0
    assert package.trust_classification == "EXPORT_WITH_WARNINGS"
    assert package.export_classification == "EXPORT_WITH_WARNINGS"
    assert package.reconstruction_status == "RECONSTRUCTABLE"
    assert package.audit_package_status == "CREATED"
    assert package.created_timestamp


@pytest.mark.parametrize(
    "kwargs",
    [
        {"trust_record_reference": ""},
        {"evidence_lineage_reference": ""},
        {"decision_ledger_reference": ""},
        {"decision_explanation_reference": ""},
        {"reconstruction_status": ""},
        {"audit_package_status": ""},
    ],
)
def test_audit_package_factory_rejects_missing_required_fields(kwargs):
    factory = AuditPackageFactory()
    base_kwargs = {
        "trust_record_reference": "TR-001",
        "evidence_lineage_reference": "EL-001",
        "decision_ledger_reference": "DL-001",
        "decision_explanation_reference": "DE-001",
        "rule_version_references": ["TRUST_MODEL_RULES_V1"],
        "exception_references": ["EX-001"],
        "trust_score": 85.0,
        "trust_classification": "EXPORT_WITH_WARNINGS",
        "export_classification": "EXPORT_WITH_WARNINGS",
    }
    base_kwargs.update(kwargs)

    with pytest.raises(ValueError):
        factory.create(**base_kwargs)
