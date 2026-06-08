from datetime import datetime, UTC
from uuid import uuid4

from trust_engine.domain.authoritative_models import DecisionLedgerEntry


class DecisionLedgerFactory:
    def create(
        self,
        trust_record_reference,
        decision_explanation_reference,
        rule_version_reference,
        decision_rationale,
        evidence_references,
        exception_references,
        trust_score,
        trust_classification,
        decision_outcome,
    ):
        if not decision_rationale or str(decision_rationale).strip() == "":
            raise ValueError("decision rationale is required")

        if evidence_references is None:
            raise ValueError("evidence references are required")

        if exception_references is None:
            raise ValueError("exception references are required")

        if trust_score is None:
            raise ValueError("trust score is required")

        if not trust_classification or str(trust_classification).strip() == "":
            raise ValueError("trust classification is required")

        if not decision_outcome or str(decision_outcome).strip() == "":
            raise ValueError("decision outcome is required")

        timestamp = datetime.now(UTC)

        return DecisionLedgerEntry(
            decision_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            decision_explanation_reference=decision_explanation_reference,
            rule_version_reference=rule_version_reference,
            decision_rationale=decision_rationale,
            evidence_references=list(evidence_references),
            exception_references=list(exception_references),
            trust_score=trust_score,
            trust_classification=trust_classification,
            decision_outcome=decision_outcome,
            decision_timestamp=timestamp,
            created_timestamp=timestamp,
        )