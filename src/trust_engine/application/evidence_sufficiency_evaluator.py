from dataclasses import dataclass
from datetime import datetime

from trust_engine.application.exception_record_factory import ExceptionRecordFactory
from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.severity import Severity


@dataclass
class EvidenceSufficiencyResult:
    status: str
    findings: list
    generated_exceptions: list


class EvidenceSufficiencyEvaluator:
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"
    RULE_NAME = "EVIDENCE_LINEAGE_SUFFICIENCY_REQUIREMENTS"

    REQUIRED_FIELDS = (
        "source_document_reference",
        "source_location",
        "page_reference",
        "acquisition_method",
        "evidence_hash",
        "chain_of_custody",
        "evidence_type",
        "evidence_status",
        "acquisition_timestamp",
    )

    PLACEHOLDER_VALUES = {
        "UNKNOWN_LOCATION",
        "UNKNOWN_PAGE",
        "UNKNOWN_HASH",
    }

    VERIFIABLE_EVIDENCE_STATUSES = {
        "CAPTURED",
        "VERIFIED",
        "AUTHENTICATED",
    }

    def __init__(self, exception_record_factory=None, policy=None):
        self.exception_record_factory = exception_record_factory or ExceptionRecordFactory()
        self.policy = policy or TrustModelPolicy()

    def evaluate(self, evidence_lineage):
        findings = []

        for field_name in self.REQUIRED_FIELDS:
            value = getattr(evidence_lineage, field_name, None)
            if self._is_missing(value):
                findings.append(
                    self._finding(
                        field_name,
                        value,
                        "required evidence lineage field is missing or blank",
                    )
                )

        for field_name in ("source_location", "page_reference", "evidence_hash"):
            value = getattr(evidence_lineage, field_name, None)
            if value in self.PLACEHOLDER_VALUES:
                findings.append(
                    self._finding(
                        field_name,
                        value,
                        f"{field_name} uses placeholder value",
                    )
                )

        evidence_status = getattr(evidence_lineage, "evidence_status", None)
        if (
            not self._is_missing(evidence_status)
            and evidence_status not in self.VERIFIABLE_EVIDENCE_STATUSES
        ):
            findings.append(
                self._finding(
                    "evidence_status",
                    evidence_status,
                    "evidence status is not verifiable",
                )
            )

        acquisition_timestamp = getattr(evidence_lineage, "acquisition_timestamp", None)
        if acquisition_timestamp is not None and not isinstance(
            acquisition_timestamp, datetime
        ):
            findings.append(
                self._finding(
                    "acquisition_timestamp",
                    acquisition_timestamp,
                    "acquisition timestamp is not valid acquisition metadata",
                )
            )

        generated_exceptions = [
            self._exception_for(evidence_lineage, finding) for finding in findings
        ]

        status = self.SUFFICIENT if not findings else self.INSUFFICIENT

        return EvidenceSufficiencyResult(
            status=status,
            findings=findings,
            generated_exceptions=generated_exceptions,
        )

    def _is_missing(self, value):
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, list) and len(value) == 0:
            return True
        return False

    def _finding(self, field_name, observed_value, rationale):
        return {
            "field_name": field_name,
            "observed_value": observed_value,
            "rationale": rationale,
            "remediation_guidance": (
                "Provide complete, non-placeholder evidence lineage metadata capable "
                "of supporting trust certification and courtroom reconstruction."
            ),
        }

    def _exception_for(self, evidence_lineage, finding):
        severity = Severity.WARNING
        penalty = self.policy.penalty_for(severity)

        return self.exception_record_factory.create(
            severity.value,
            penalty,
            self.RULE_NAME,
            source_reference=getattr(evidence_lineage, "lineage_id", "UNKNOWN_LINEAGE"),
            field_name=finding["field_name"],
            original_value=str(finding["observed_value"]),
            expected_value="SUFFICIENT_EVIDENCE_LINEAGE",
            exception_reason=finding["rationale"],
            remediation_guidance=finding["remediation_guidance"],
            status="ACTIVE",
            active=True,
        )
