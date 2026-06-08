from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import EvidenceLineageRecord


class EvidenceLineageFactory:
    REQUIRED_FIELDS = {
        "source_document_reference": "source document reference is required",
        "source_location": "source location is required",
        "page_reference": "page reference is required",
        "acquisition_method": "acquisition method is required",
        "evidence_hash": "evidence hash is required",
        "evidence_type": "evidence type is required",
        "evidence_status": "evidence status is required",
    }

    def create(
        self,
        source_document_reference,
        source_location="UNKNOWN_LOCATION",
        page_reference="UNKNOWN_PAGE",
        acquisition_method="SYSTEM_CAPTURE",
        evidence_hash="UNKNOWN_HASH",
        chain_of_custody=None,
        evidence_type="SOURCE_DOCUMENT",
        evidence_status="CAPTURED",
        lineage_version="1.0.0",
    ):
        values = {
            "source_document_reference": source_document_reference,
            "source_location": source_location,
            "page_reference": page_reference,
            "acquisition_method": acquisition_method,
            "evidence_hash": evidence_hash,
            "evidence_type": evidence_type,
            "evidence_status": evidence_status,
        }

        for field_name, message in self.REQUIRED_FIELDS.items():
            value = values[field_name]
            if value is None or str(value).strip() == "":
                raise ValueError(message)

        timestamp = datetime.now(UTC)

        return EvidenceLineageRecord(
            lineage_id=str(uuid4()),
            lineage_version=lineage_version,
            source_document_reference=source_document_reference,
            source_location=source_location,
            page_reference=page_reference,
            acquisition_method=acquisition_method,
            acquisition_timestamp=timestamp,
            evidence_hash=evidence_hash,
            chain_of_custody=chain_of_custody or [],
            evidence_type=evidence_type,
            evidence_status=evidence_status,
            created_timestamp=timestamp,
        )