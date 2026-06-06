from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import TrustRecord

class TrustRecordFactory:
    def create(self, trust_score, trust_classification, evidence_count=0, exception_count=0, exception_penalty=0.0, embargo=False, trust_calculation_rule="EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY"):
        return TrustRecord(
            trust_record_id=str(uuid4()),
            trust_score=trust_score,
            trust_classification=trust_classification,
            evidence_count=evidence_count,
            exception_count=exception_count,
            exception_penalty=exception_penalty,
            embargo=embargo,
            trust_calculation_rule=trust_calculation_rule,
            created_timestamp=datetime.now(UTC)
        )
