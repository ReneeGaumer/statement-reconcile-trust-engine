from trust_engine.exceptions.severity import Severity

class ExportEmbargoEvaluator:
    def should_embargo(self, severities):
        return Severity.CRITICAL in severities
