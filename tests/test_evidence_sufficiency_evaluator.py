from datetime import UTC, datetime

from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory
from trust_engine.application.evidence_sufficiency_evaluator import (
    EvidenceSufficiencyEvaluator,
)


def complete_lineage():
    return EvidenceLineageFactory().create(
        "statement.pdf",
        source_location="bank-portal",
        page_reference="page-1",
        acquisition_method="UPLOAD",
        evidence_hash="hash-001",
        chain_of_custody=["uploaded-by-user"],
        evidence_type="BANK_STATEMENT",
        evidence_status="CAPTURED",
    )


def test_sufficient_evidence_lineage_returns_sufficient_without_exceptions():
    evaluator = EvidenceSufficiencyEvaluator()

    result = evaluator.evaluate(complete_lineage())

    assert result.status == "SUFFICIENT"
    assert result.findings == []
    assert result.generated_exceptions == []


def test_placeholder_lineage_generates_exception_records():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = EvidenceLineageFactory().create("statement.pdf")

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert result.findings
    assert result.generated_exceptions
    assert all(
        exception.rule_name == evaluator.RULE_NAME
        for exception in result.generated_exceptions
    )
    assert all(
        exception.source_reference == lineage.lineage_id
        for exception in result.generated_exceptions
    )


def test_missing_source_location_generates_exception():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = complete_lineage()
    lineage.source_location = None

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert any(finding["field_name"] == "source_location" for finding in result.findings)
    assert any(
        exception.field_name == "source_location"
        for exception in result.generated_exceptions
    )


def test_missing_page_reference_generates_exception():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = complete_lineage()
    lineage.page_reference = None

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert any(finding["field_name"] == "page_reference" for finding in result.findings)
    assert any(
        exception.field_name == "page_reference"
        for exception in result.generated_exceptions
    )


def test_missing_evidence_hash_generates_exception():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = complete_lineage()
    lineage.evidence_hash = None

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert any(finding["field_name"] == "evidence_hash" for finding in result.findings)
    assert any(
        exception.field_name == "evidence_hash"
        for exception in result.generated_exceptions
    )


def test_empty_chain_of_custody_generates_exception():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = complete_lineage()
    lineage.chain_of_custody = []

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert any(
        finding["field_name"] == "chain_of_custody" for finding in result.findings
    )
    assert any(
        exception.field_name == "chain_of_custody"
        for exception in result.generated_exceptions
    )


def test_unverifiable_evidence_status_generates_exception():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = complete_lineage()
    lineage.evidence_status = "UNVERIFIED"

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert any(finding["field_name"] == "evidence_status" for finding in result.findings)
    assert any(
        exception.field_name == "evidence_status"
        for exception in result.generated_exceptions
    )


def test_missing_acquisition_metadata_generates_exception():
    evaluator = EvidenceSufficiencyEvaluator()
    lineage = complete_lineage()
    lineage.acquisition_timestamp = None

    result = evaluator.evaluate(lineage)

    assert result.status == "INSUFFICIENT"
    assert any(
        finding["field_name"] == "acquisition_timestamp"
        for finding in result.findings
    )
    assert any(
        exception.field_name == "acquisition_timestamp"
        for exception in result.generated_exceptions
    )


def test_evidence_sufficiency_does_not_assign_trust_classification():
    evaluator = EvidenceSufficiencyEvaluator()

    result = evaluator.evaluate(complete_lineage())

    assert not hasattr(result, "trust_classification")
    assert not hasattr(result, "export_classification")
    assert not hasattr(evaluator, "classify")
    assert not hasattr(evaluator, "calculate")