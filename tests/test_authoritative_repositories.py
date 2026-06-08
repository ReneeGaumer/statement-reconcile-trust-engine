from trust_engine.application.trust_record_factory import TrustRecordFactory
from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory
from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory
from trust_engine.application.audit_package_factory import AuditPackageFactory
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository
from trust_engine.infrastructure.decision_ledger_repository import DecisionLedgerRepository
from trust_engine.infrastructure.evidence_lineage_repository import EvidenceLineageRepository
from trust_engine.infrastructure.audit_package_repository import AuditPackageRepository


def test_authoritative_repositories():
    trust_record = TrustRecordFactory().create(100.0, "CLEAN_EXPORT")
    evidence = EvidenceLineageFactory().create("statement.pdf")
    ledger = DecisionLedgerFactory().create(
        trust_record_reference=trust_record.trust_record_id,
        decision_explanation_reference="DE-001",
        rule_version_reference="TRUST_MODEL_RULES_V1",
        decision_rationale="Repository persistence test decision rationale.",
        evidence_references=[evidence.lineage_id],
        exception_references=[],
        trust_score=trust_record.trust_score,
        trust_classification=trust_record.trust_classification,
        decision_outcome=trust_record.trust_classification,
    )
    audit = AuditPackageFactory().create(
        trust_record.trust_record_id,
        evidence.lineage_id,
        ledger.decision_id,
    )

    repos = [
        (TrustRecordRepository(), trust_record, trust_record.trust_record_id),
        (EvidenceLineageRepository(), evidence, evidence.lineage_id),
        (DecisionLedgerRepository(), ledger, ledger.decision_id),
        (AuditPackageRepository(), audit, audit.audit_package_id),
    ]

    for repo, record, record_id in repos:
        saved = repo.save(record)
        loaded = repo.get(record_id)
        print(saved)
        assert loaded == record
        try:
            repo.save(record)
            raise AssertionError("Overwrite should have failed")
        except ValueError:
            print("Immutable save protection confirmed", record_id)