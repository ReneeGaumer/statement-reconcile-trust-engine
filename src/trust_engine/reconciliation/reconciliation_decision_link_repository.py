class ReconciliationDecisionLinkRepository:
    def __init__(self):
        self.links = {}

    def save(self, reconciliation_decision_link):
        if reconciliation_decision_link.reconciliation_decision_link_id in self.links:
            raise ValueError(
                "Reconciliation decision link already exists and cannot be overwritten: "
                + reconciliation_decision_link.reconciliation_decision_link_id
            )

        self.links[
            reconciliation_decision_link.reconciliation_decision_link_id
        ] = reconciliation_decision_link

    def get(self, reconciliation_decision_link_id):
        return self.links.get(reconciliation_decision_link_id)

    def list_all(self):
        return list(self.links.values())