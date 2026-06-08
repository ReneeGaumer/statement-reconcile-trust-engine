class ReconciliationTrustImpactEvaluator:
    def __init__(self, policy):
        self.policy = policy

    def severities_for(self, reconciliation_records):
        trust_impact_statuses = self.policy.reconciliation_trust_impact_statuses()
        trust_impact_severity = self.policy.reconciliation_trust_impact_severity()

        return [
            trust_impact_severity
            for record in reconciliation_records
            if record.status in trust_impact_statuses
        ]