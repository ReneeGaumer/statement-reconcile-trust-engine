from datetime import datetime, UTC
from uuid import uuid4

from trust_engine.domain.authoritative_models import AuditPackage


class AuditPackageFactory:
    def create(
        self,
        trust_record_reference,
        evidence_lineage_reference,
        decision_ledger_reference,
        decision_explanation_reference=None,
        rule_version_references=None,
        exception_references=None,
        trust_score=None,
        trust_classification=None,
        export_classification=None,
        reconstruction_status="RECONSTRUCTABLE",
        audit_package_status="CREATED",
    ):
        if not trust_record_reference or str(trust_record_reference).strip() == "":
            raise ValueError("trust record reference is required")
        if not evidence_lineage_reference or str(evidence_lineage_reference).strip() == "":
            raise ValueError("evidence lineage reference is required")
        if not decision_ledger_reference or str(decision_ledger_reference).strip() == "":
            raise ValueError("decision ledger reference is required")
        if decision_explanation_reference is not None and str(decision_explanation_reference).strip() == "":
            raise ValueError("decision explanation reference cannot be blank")
        if reconstruction_status is None or str(reconstruction_status).strip() == "":
            raise ValueError("reconstruction status is required")
        if audit_package_status is None or str(audit_package_status).strip() == "":
            raise ValueError("audit package status is required")

        return AuditPackage(
            audit_package_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            evidence_lineage_reference=evidence_lineage_reference,
            decision_ledger_reference=decision_ledger_reference,
            decision_explanation_reference=decision_explanation_reference,
            rule_version_references=list(rule_version_references or []),
            exception_references=list(exception_references or []),
            trust_score=trust_score,
            trust_classification=trust_classification,
            export_classification=export_classification,
            reconstruction_status=reconstruction_status,
            audit_package_status=audit_package_status,
            created_timestamp=datetime.now(UTC),
        )
