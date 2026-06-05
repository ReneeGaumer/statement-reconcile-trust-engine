from trust_engine.exceptions.severity import Severity

class ExceptionEvaluator:
    def penalty(self, severity: Severity) -> float:
        penalties = {
            Severity.INFO: 0.0,
            Severity.WARNING: 5.0,
            Severity.HIGH: 20.0,
            Severity.CRITICAL: 50.0,
        }
        return penalties[severity]
