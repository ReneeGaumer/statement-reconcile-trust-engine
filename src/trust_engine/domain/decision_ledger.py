from dataclasses import dataclass

@dataclass(frozen=True)
class DecisionLedger:
    decision_id: str
    decision_rationale: str
