from trust_engine.application.audit_package_factory import AuditPackageFactory
from trust_engine.application.decision_explanation_factory import DecisionExplanationFactory
from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory
from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory
from trust_engine.application.exception_record_factory import ExceptionRecordFactory
from trust_engine.application.export_package_factory import ExportPackageFactory
from trust_engine.application.trust_record_factory import TrustRecordFactory
from trust_engine.infrastructure.audit_package_repository import AuditPackageRepository
from trust_engine.infrastructure.decision_explanation_repository import (
    DecisionExplanationRepository,
)
from trust_engine.infrastructure.decision_ledger_repository import DecisionLedgerRepository
from trust_engine.infrastructure.evidence_lineage_repository import EvidenceLineageRepository
from trust_engine.infrastructure.exception_record_repository import ExceptionRecordRepository
from trust_engine.infrastructure.export_package_repository import ExportPackageRepository
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository


def build_repository_cases():
    trust_record = TrustRecordFactory().create(
        90.0,
        "EXPORT_WITH_WARNINGS",
        evidence_count=10,
        exception_count=1,
        exception_penalty=10,
        embargo=False,
        trust_calculation_rule="TEST_RULE",
        evidence_lineage_reference="EL-001",
        exception_record_references=["EX-001"],
    )

    evidence_lineage = EvidenceLineageFactory().create(
        "statement.pdf",
        source_location="bank-portal",
        page_reference="page-1",
        acquisition_method="UPLOAD",
        evidence_hash="hash-001",
        chain_of_custody=["uploaded-by-user"],
        evidence_type="BANK_STATEMENT",
        evidence_status="CAPTURED",
    )

    decision_explanation = DecisionExplanationFactory().create(
    trust_record.trust_record_id,
    evidence_count=10,
    exception_count=1,
    exception_penalty=10,
    embargo=False,
    trust_score=90.0,
    trust_classification="EXPORT_WITH_WARNINGS",
    decision_path=[
        {
            "step": "TRUST_SCORE_CALCULATED",
            "rule": "TEST_RULE",
            "inputs": {"evidence_count": 10, "exception_penalty": 10},
            "output": 90.0,
        }
    ],
    exception_record_references=["EX-001"],
)

    decision_ledger = DecisionLedgerFactory().create(
        trust_record_reference=trust_record.trust_record_id,
        decision_explanation_reference=decision_explanation.decision_explanation_id,
        rule_version_reference="TRUST_MODEL_RULES_V1",
        decision_rationale="Repository contract test rationale.",
        evidence_references=[evidence_lineage.lineage_id],
        exception_references=["EX-001"],
        trust_score=90.0,
        trust_classification="EXPORT_WITH_WARNINGS",
        decision_outcome="EXPORT_WITH_WARNINGS",
    )

    audit_package = AuditPackageFactory().create(
        trust_record.trust_record_id,
        evidence_lineage.lineage_id,
        decision_ledger.decision_id,
        decision_explanation.decision_explanation_id,
        ["TRUST_MODEL_RULES_V1"],
        ["EX-001"],
        90.0,
        "EXPORT_WITH_WARNINGS",
        "EXPORT_WITH_WARNINGS",
    )

    exception_record = ExceptionRecordFactory().create(
        "WARNING",
        10,
        "WARNING_EXCEPTION_RULE",
        source_reference="statement.pdf",
        field_name="amount",
        original_value="100.00",
        expected_value="100.00",
        exception_reason="Repository contract test exception.",
    )

    export_package = ExportPackageFactory().create(
        trust_record.trust_record_id,
        audit_package.audit_package_id,
        "EXPORT_WITH_WARNINGS",
    )

    return [
        (TrustRecordRepository(), trust_record, trust_record.trust_record_id, "trust_score", 0.0),
        (
            EvidenceLineageRepository(),
            evidence_lineage,
            evidence_lineage.lineage_id,
            "source_document_reference",
            "mutated.pdf",
        ),
        (
            DecisionExplanationRepository(),
            decision_explanation,
            decision_explanation.decision_explanation_id,
            "trust_score",
            0.0,
        ),
        (
            DecisionLedgerRepository(),
            decision_ledger,
            decision_ledger.decision_id,
            "decision_rationale",
            "mutated rationale",
        ),
        (
            AuditPackageRepository(),
            audit_package,
            audit_package.audit_package_id,
            "audit_package_status",
            "MUTATED",
        ),
        (
            ExceptionRecordRepository(),
            exception_record,
            exception_record.exception_id,
            "penalty",
            999,
        ),
        (
            ExportPackageRepository(),
            export_package,
            export_package.export_package_id,
            "export_classification",
            "UNSAFE_EXPORT",
        ),
    ]


def test_authoritative_repositories_are_append_only():
    for repo, record, record_id, _field_name, _mutated_value in build_repository_cases():
        repo.save(record)

        try:
            repo.save(record)
            raise AssertionError("overwrite should have failed")
        except ValueError:
            pass

        assert repo.get(record_id) == record


def test_authoritative_repositories_protect_saved_records_from_original_mutation():
    for repo, record, record_id, field_name, mutated_value in build_repository_cases():
        original_value = getattr(record, field_name)

        repo.save(record)
        setattr(record, field_name, mutated_value)

        loaded = repo.get(record_id)

        assert getattr(loaded, field_name) == original_value
        assert getattr(loaded, field_name) != mutated_value


def test_authoritative_repositories_protect_stored_records_from_loaded_mutation():
    for repo, record, record_id, field_name, mutated_value in build_repository_cases():
        original_value = getattr(record, field_name)

        repo.save(record)
        loaded = repo.get(record_id)
        setattr(loaded, field_name, mutated_value)

        loaded_again = repo.get(record_id)

        assert getattr(loaded_again, field_name) == original_value
        assert getattr(loaded_again, field_name) != mutated_value


def test_authoritative_repository_all_returns_defensive_copies():
    for repo, record, record_id, field_name, mutated_value in build_repository_cases():
        original_value = getattr(record, field_name)

        repo.save(record)
        all_records = repo.all()
        setattr(all_records[0], field_name, mutated_value)

        loaded_again = repo.get(record_id)

        assert getattr(loaded_again, field_name) == original_value
        assert getattr(loaded_again, field_name) != mutated_value