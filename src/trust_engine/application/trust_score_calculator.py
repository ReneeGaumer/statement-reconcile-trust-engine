class TrustScoreCalculator:
    def calculate(self, evidence_count: int, exception_penalty: float) -> float:
        score = max(0.0, min(100.0, evidence_count * 10.0 - exception_penalty))
        return round(score, 2)
