from trust_engine.exceptions.severity import Severity


class TrustModelPolicy:
    RULE_VERSION_REFERENCE = "TRUST_MODEL_RULES_V1"

    SEVERITY_PENALTIES = {
        Severity.INFO: 0.0,
        Severity.WARNING: 5.0,
        Severity.HIGH: 20.0,
        Severity.CRITICAL: 50.0,
    }

    CLASSIFICATION_THRESHOLDS = [
        (90.0, "CLEAN_EXPORT"),
        (75.0, "EXPORT_WITH_WARNINGS"),
        (50.0, "PARTIAL_EXPORT"),
    ]

    EMBARGO_CLASSIFICATION = "EXPORT_EMBARGO"
    UNSAFE_CLASSIFICATION = "UNSAFE_EXPORT"

    SCORE_CALCULATION_RULE = "EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY"
    EMBARGO_RULE = "CRITICAL_SEVERITY_TRIGGERS_EXPORT_EMBARGO"
    CLASSIFICATION_RULE = "TRUST_SCORE_THRESHOLD_WITH_EMBARGO_OVERRIDE"
    EXCEPTION_PENALTY_RULE = "SEVERITY_TO_EXCEPTION_PENALTY"

    def penalty_for(self, severity: Severity) -> float:
        return self.SEVERITY_PENALTIES[severity]

    def should_embargo(self, severities) -> bool:
        return Severity.CRITICAL in severities

    def classify(self, score: float, embargo: bool = False) -> str:
        if embargo:
            return self.EMBARGO_CLASSIFICATION

        for minimum_score, classification in self.CLASSIFICATION_THRESHOLDS:
            if score >= minimum_score:
                return classification

        return self.UNSAFE_CLASSIFICATION