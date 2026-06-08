from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class ReconciliationDecisionLink:
    reconciliation_decision_link_id: str
    trust_record_reference: str
    decision_explanation_reference: str
    reconciliation_record_references: list
    source_document_reference: str
    rule_reference: str
    created_timestamp: str

    @classmethod
    def create(
        cls,
        trust_record_reference,
        decision_explanation_reference,
        reconciliation_record_references,
        source_document_reference,
        rule_reference,
    ):
        return cls(
            reconciliation_decision_link_id="RECONCILIATION-DECISION-LINK-"
            + str(uuid4()),
            trust_record_reference=trust_record_reference,
            decision_explanation_reference=decision_explanation_reference,
            reconciliation_record_references=list(reconciliation_record_references),
            source_document_reference=source_document_reference,
            rule_reference=rule_reference,
            created_timestamp=datetime.now(timezone.utc).isoformat(),
        )