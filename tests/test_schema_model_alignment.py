import json
from dataclasses import fields
from pathlib import Path

from trust_engine.domain.authoritative_models import (
    AuditPackage,
    DecisionLedgerEntry,
    EvidenceLineageRecord,
    ExceptionRecordV2,
    TrustRecord,
)


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dataclass_field_names(model):
    return {field.name for field in fields(model)}


def required_schema_concepts(schema):
    return {
        key.removesuffix("_required")
        for key, value in schema.items()
        if key.endswith("_required") and value is True
    }


def assert_required_schema_concepts_are_represented(schema_path, model, schema_to_model):
    schema = load_json(schema_path)
    model_fields = dataclass_field_names(model)

    missing = []
    for schema_concept in required_schema_concepts(schema):
        model_field = schema_to_model.get(schema_concept, schema_concept)
        if model_field not in model_fields:
            missing.append(
                {
                    "schema_concept": schema_concept,
                    "expected_model_field": model_field,
                    "model": model.__name__,
                }
            )

    assert missing == []


def test_trust_record_schema_required_concepts_are_represented():
    assert_required_schema_concepts_are_represented(
        "architecture/data/trust-record.schema.json",
        TrustRecord,
        {
            "record_id": "trust_record_id",
            "export_eligibility": "trust_classification",
            "decision_ledger_reference": "trust_record_id",
        },
    )


def test_evidence_lineage_schema_required_concepts_are_represented():
    assert_required_schema_concepts_are_represented(
        "architecture/data/evidence-lineage-fields.schema.json",
        EvidenceLineageRecord,
        {
            "source_document": "source_document_reference",
            "evidence_timestamp": "acquisition_timestamp",
        },
    )


def test_decision_ledger_schema_required_concepts_are_represented():
    assert_required_schema_concepts_are_represented(
        "architecture/data/decision-ledger-fields.schema.json",
        DecisionLedgerEntry,
        {
            "record_id": "trust_record_reference",
            "deterministic_rule_reference": "rule_version_reference",
            "evidence_lineage_reference": "evidence_references",
        },
    )


def test_audit_package_schema_required_concepts_are_represented():
    assert_required_schema_concepts_are_represented(
        "architecture/data/audit-package.schema.json",
        AuditPackage,
        {
            "package_id": "audit_package_id",
            "generated_timestamp": "created_timestamp",
            "courtroom_test": "reconstruction_status",
        },
    )


def test_exception_record_schema_required_concepts_are_represented():
    assert_required_schema_concepts_are_represented(
        "architecture/data/exception-record.schema.json",
        ExceptionRecordV2,
        {
            "record_id": "source_reference",
            "rule_reference": "rule_name",
            "evidence_reference": "source_reference",
            "description": "exception_reason",
            "status": "severity",
        },
    )


def test_export_embargo_schema_declares_hard_stop():
    schema = load_json("trust-model/classifications/export-embargo.schema.json")

    assert schema["classification_id"] == "EXPORT_EMBARGO"
    assert schema["severity"] == "CRITICAL"
    assert schema["hard_stop"] is True