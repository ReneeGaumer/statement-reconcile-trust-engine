from trust_engine.application.trust_model_policy import TrustModelPolicy


class ExportEmbargoEvaluator:
    def __init__(self, policy=None):
        self.policy = policy or TrustModelPolicy()

    def should_embargo(self, severities):
        return self.policy.should_embargo(severities)