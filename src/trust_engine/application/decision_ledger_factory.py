from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import DecisionLedgerEntry

class DecisionLedgerFactory:
    def create(self, trust_record_reference, decision_explanation_reference="", rule_version_reference="TRUST_MODEL_RULES_V1"):
        return DecisionLedgerEntry(
            decision_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            decision_explanation_reference=decision_explanation_reference,
            rule_version_reference=rule_version_reference,
            decision_timestamp=datetime.now(UTC)
        )
