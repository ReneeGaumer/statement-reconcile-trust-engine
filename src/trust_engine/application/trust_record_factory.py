from datetime import datetime
from uuid import uuid4
from trust_engine.domain.authoritative_models import TrustRecord

class TrustRecordFactory:
    def create(self, trust_score, trust_classification):
        return TrustRecord(
            trust_record_id=str(uuid4()),
            trust_score=trust_score,
            trust_classification=trust_classification,
            created_timestamp=datetime.utcnow()
        )
