from datetime import datetime
from uuid import uuid4
from trust_engine.domain.authoritative_models import AuditPackage

class AuditPackageFactory:
    def create(self, trust_record_reference, evidence_lineage_reference, decision_ledger_reference):
        return AuditPackage(
            audit_package_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            evidence_lineage_reference=evidence_lineage_reference,
            decision_ledger_reference=decision_ledger_reference,
            created_timestamp=datetime.utcnow()
        )
