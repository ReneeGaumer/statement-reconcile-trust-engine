from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import EvidenceLineageRecord

class EvidenceLineageFactory:
    def create(self, source_document_reference):
        return EvidenceLineageRecord(
            lineage_id=str(uuid4()),
            source_document_reference=source_document_reference,
            acquisition_timestamp=datetime.now(UTC)
        )
