from datetime import datetime, UTC
from uuid import uuid4

from trust_engine.domain.authoritative_models import DecisionExplanationRecord


class DecisionExplanationFactory:
    def create(
        self,
        trust_record_reference,
        evidence_count,
        exception_count,
        exception_penalty,
        embargo,
        trust_score,
        trust_classification,
        decision_path,
        exception_record_references=None,
    ):
        if not trust_record_reference or str(trust_record_reference).strip() == "":
            raise ValueError("trust record reference is required")
        if evidence_count is None:
            raise ValueError("evidence count is required")
        if exception_count is None:
            raise ValueError("exception count is required")
        if exception_penalty is None:
            raise ValueError("exception penalty is required")
        if embargo is None:
            raise ValueError("embargo value is required")
        if trust_score is None:
            raise ValueError("trust score is required")
        if not trust_classification or str(trust_classification).strip() == "":
            raise ValueError("trust classification is required")
        if not decision_path:
            raise ValueError("decision path is required")

        for step in decision_path:
            if not step.get("step"):
                raise ValueError("decision path step is required")
            if not step.get("rule"):
                raise ValueError("decision path rule is required")
            if "inputs" not in step:
                raise ValueError("decision path inputs are required")
            if "output" not in step:
                raise ValueError("decision path output is required")

        return DecisionExplanationRecord(
            decision_explanation_id=str(uuid4()),
            trust_record_reference=trust_record_reference,
            evidence_count=evidence_count,
            exception_count=exception_count,
            exception_penalty=exception_penalty,
            embargo=embargo,
            trust_score=trust_score,
            trust_classification=trust_classification,
            exception_record_references=exception_record_references or [],
            decision_path=decision_path,
            created_timestamp=datetime.now(UTC),
        )