from trust_engine.application.trust_record_factory import TrustRecordFactory
from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory
from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory
from trust_engine.application.audit_package_factory import AuditPackageFactory
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository
from trust_engine.infrastructure.decision_ledger_repository import DecisionLedgerRepository
from trust_engine.infrastructure.evidence_lineage_repository import EvidenceLineageRepository
from trust_engine.infrastructure.audit_package_repository import AuditPackageRepository

trust_record = TrustRecordFactory().create(100.0, "CLEAN_EXPORT")
evidence = EvidenceLineageFactory().create("statement.pdf")
ledger = DecisionLedgerFactory().create(trust_record.trust_record_id)
audit = AuditPackageFactory().create(trust_record.trust_record_id, evidence.lineage_id, ledger.decision_id)

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

print("PASS")
