import json
from pathlib import Path

from trust_engine.exceptions.severity import Severity


class TrustModelPolicy:
    RULE_VERSION_REFERENCE = "TRUST_MODEL_RULES_V1"

    TRUST_MODEL_DIR = Path("trust-model/classifications")
    TRUST_IMPACT_RULES_PATH = TRUST_MODEL_DIR / "trust-impact-rules.schema.json"
    CLASSIFICATION_THRESHOLDS_PATH = (
        TRUST_MODEL_DIR / "trust-classification-thresholds.schema.json"
    )

    EMBARGO_CLASSIFICATION = "EXPORT_EMBARGO"
    UNSAFE_CLASSIFICATION = "UNSAFE_EXPORT"

    SCORE_CALCULATION_RULE = "EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY"
    EMBARGO_RULE = "CRITICAL_SEVERITY_TRIGGERS_EXPORT_EMBARGO"
    CLASSIFICATION_RULE = "TRUST_SCORE_THRESHOLD_WITH_EMBARGO_OVERRIDE"
    EXCEPTION_PENALTY_RULE = "SEVERITY_TO_EXCEPTION_PENALTY"

    def __init__(self):
        self.severity_penalties = self._load_severity_penalties()
        self.classification_thresholds = self._load_classification_thresholds()

    def penalty_for(self, severity: Severity) -> float:
        return self.severity_penalties[severity]

    def should_embargo(self, severities) -> bool:
        return Severity.CRITICAL in severities

    def classify(self, score: float, embargo: bool = False) -> str:
        if embargo:
            return self.EMBARGO_CLASSIFICATION

        for minimum_score, classification in self.classification_thresholds:
            if score >= minimum_score:
                return classification

        return self.UNSAFE_CLASSIFICATION

    def _load_json(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_severity_penalties(self):
        impact_rules = self._load_json(self.TRUST_IMPACT_RULES_PATH)

        return {
            Severity.INFO: abs(float(impact_rules["INFO"])),
            Severity.WARNING: abs(float(impact_rules["WARNING"])),
            Severity.HIGH: abs(float(impact_rules["HIGH"])),
            Severity.CRITICAL: abs(float(impact_rules["CRITICAL"])),
        }

    def _load_classification_thresholds(self):
        threshold_rules = self._load_json(self.CLASSIFICATION_THRESHOLDS_PATH)

        return [
            (100.0, threshold_rules["100"]),
            (85.0, threshold_rules["85-99"]),
            (60.0, threshold_rules["60-84"]),
            (1.0, threshold_rules["1-59"]),
        ]