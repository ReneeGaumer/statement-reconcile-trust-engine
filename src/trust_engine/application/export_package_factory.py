from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import ExportPackage


class ExportPackageFactory:
    EMBARGO_CLASSIFICATION = "EXPORT_EMBARGO"

    def create(self, trust_record_reference, audit_package_reference, export_classification):
        if export_classification == self.EMBARGO_CLASSIFICATION:
            raise ValueError("EXPORT_EMBARGO is a hard stop; export package creation is prohibited")

        return ExportPackage(
            export_package_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            audit_package_reference=audit_package_reference,
            export_classification=export_classification,
            created_timestamp=datetime.now(UTC)
        )
