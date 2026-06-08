from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.trust_classification import TrustClassification


class TrustClassifier:
    def __init__(self, policy=None):
        self.policy = policy or TrustModelPolicy()

    def classify(self, score: float, embargo: bool = False):
        classification = self.policy.classify(score, embargo)
        return TrustClassification(classification)