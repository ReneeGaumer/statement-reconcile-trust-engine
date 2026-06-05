from dataclasses import dataclass

@dataclass(frozen=True)
class TrustRecord:
    trust_record_id: str
    trust_score: float
    trust_classification: str
