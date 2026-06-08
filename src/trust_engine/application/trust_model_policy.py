import json
from pathlib import Path

from trust_engine.exceptions.severity import Severity


class TrustModelPolicy:
    RULE_VERSION_REFERENCE = "TRUST_MODEL_RULES_V1"

    DEFAULT_TRUST_MODEL_DIR = Path("trust-model/classifications")
    TRUST_IMPACT_RULES_FILE = "trust-impact-rules.schema.json"
    CLASSIFICATION_THRESHOLDS_FILE = "trust-classification-thresholds.schema.json"

    EMBARGO_CLASSIFICATION = "EXPORT_EMBARGO"
    UNSAFE_CLASSIFICATION = "UNSAFE_EXPORT"

    SCORE_CALCULATION_RULE = "EVIDENCE_COUNT_TIMES_TEN_MINUS_EXCEPTION_PENALTY"
    EMBARGO_RULE = "CRITICAL_SEVERITY_TRIGGERS_EXPORT_EMBARGO"
    CLASSIFICATION_RULE = "TRUST_SCORE_THRESHOLD_WITH_EMBARGO_OVERRIDE"
    EXCEPTION_PENALTY_RULE = "SEVERITY_TO_EXCEPTION_PENALTY"

    REQUIRED_IMPACT_KEYS = ("INFO", "WARNING", "HIGH", "CRITICAL")
    REQUIRED_THRESHOLD_KEYS = ("100", "85-99", "60-84", "1-59")

    def __init__(self, trust_model_dir=None):
        self.trust_model_dir = Path(trust_model_dir) if trust_model_dir else self.DEFAULT_TRUST_MODEL_DIR
        self.trust_impact_rules_path = self.trust_model_dir / self.TRUST_IMPACT_RULES_FILE
        self.classification_thresholds_path = self.trust_model_dir / self.CLASSIFICATION_THRESHOLDS_FILE
        self.severity_penalties = self._load_severity_penalties()
        self.classification_thresholds = self._load_classification_thresholds()

    def penalty_for(self, severity: Severity) -> float:
        return self.severity_penalties[severity]

    def should_embargo(self, severities) -> bool:
        return Severity.CRITICAL in severities

    def policy_source_metadata(self):
        return {
            "rule_version_reference": self.RULE_VERSION_REFERENCE,
            "trust_impact_rules_path": str(self.trust_impact_rules_path),
            "classification_thresholds_path": str(self.classification_thresholds_path),
        }

    def classify(self, score: float, embargo: bool = False) -> str:
        if embargo:
            return self.EMBARGO_CLASSIFICATION

        for minimum_score, classification in self.classification_thresholds:
            if score >= minimum_score:
                return classification

        return self.UNSAFE_CLASSIFICATION

    def _load_json(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Trust model policy file not found: {path}")

        return json.loads(path.read_text(encoding="utf-8"))

    def _require_keys(self, data, required_keys, path):
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            raise KeyError(
                f"Trust model policy file {path} is missing required keys: {missing_keys}"
            )

    def _load_severity_penalties(self):
        impact_rules = self._load_json(self.trust_impact_rules_path)
        self._require_keys(
            impact_rules,
            self.REQUIRED_IMPACT_KEYS,
            self.trust_impact_rules_path,
        )

        return {
            Severity.INFO: abs(float(impact_rules["INFO"])),
            Severity.WARNING: abs(float(impact_rules["WARNING"])),
            Severity.HIGH: abs(float(impact_rules["HIGH"])),
            Severity.CRITICAL: abs(float(impact_rules["CRITICAL"])),
        }

    def _load_classification_thresholds(self):
        threshold_rules = self._load_json(self.classification_thresholds_path)
        self._require_keys(
            threshold_rules,
            self.REQUIRED_THRESHOLD_KEYS,
            self.classification_thresholds_path,
        )

        return [
            (100.0, threshold_rules["100"]),
            (85.0, threshold_rules["85-99"]),
            (60.0, threshold_rules["60-84"]),
            (1.0, threshold_rules["1-59"]),
        ]