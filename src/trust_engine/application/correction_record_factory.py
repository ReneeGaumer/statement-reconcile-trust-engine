from datetime import UTC, datetime
from uuid import uuid4

from trust_engine.domain.authoritative_models import CorrectionRecord


class CorrectionRecordFactory:
    def create(
        self,
        original_value,
        corrected_value,
        correction_reason,
        correction_authorization_reference,
        evidence_reference,
        exception_reference,
    ):
        return CorrectionRecord(
            correction_id=f"CORR-{uuid4()}",
            original_value=original_value,
            corrected_value=corrected_value,
            correction_reason=correction_reason,
            correction_timestamp=datetime.now(UTC),
            correction_authorization_reference=correction_authorization_reference,
            evidence_reference=evidence_reference,
            exception_reference=exception_reference,
        )