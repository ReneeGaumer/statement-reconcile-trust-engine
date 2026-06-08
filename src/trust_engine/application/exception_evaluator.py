from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.exceptions.severity import Severity


class ExceptionEvaluator:
    def __init__(self, policy=None):
        self.policy = policy or TrustModelPolicy()

    def penalty(self, severity: Severity) -> float:
        return self.policy.penalty_for(severity)