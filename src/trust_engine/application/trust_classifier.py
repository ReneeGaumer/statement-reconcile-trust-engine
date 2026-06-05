from trust_engine.exceptions.trust_classification import TrustClassification

class TrustClassifier:
    def classify(self, score: float, embargo: bool = False):
        if embargo:
            return TrustClassification.EXPORT_EMBARGO
        if score >= 90:
            return TrustClassification.CLEAN_EXPORT
        if score >= 75:
            return TrustClassification.EXPORT_WITH_WARNINGS
        if score >= 50:
            return TrustClassification.PARTIAL_EXPORT
        return TrustClassification.UNSAFE_EXPORT
