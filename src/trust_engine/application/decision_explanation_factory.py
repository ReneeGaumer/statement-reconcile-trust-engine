from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import DecisionExplanationRecord

class DecisionExplanationFactory:
    def create(self, trust_record_reference, evidence_count, exception_count, exception_penalty, embargo, trust_score, trust_classification):
        return DecisionExplanationRecord(
            decision_explanation_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            evidence_count=evidence_count,
            exception_count=exception_count,
            exception_penalty=exception_penalty,
            embargo=embargo,
            trust_score=trust_score,
            trust_classification=trust_classification,
            created_timestamp=datetime.now(UTC)
        )
