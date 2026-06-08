class ReconciliationRecordRepository:
    def __init__(self):
        self.records = {}

    def save(self, reconciliation_record):
        if reconciliation_record.reconciliation_id in self.records:
            raise ValueError(
                "Reconciliation record already exists and cannot be overwritten: "
                + reconciliation_record.reconciliation_id
            )

        self.records[reconciliation_record.reconciliation_id] = reconciliation_record

    def get(self, reconciliation_id):
        return self.records.get(reconciliation_id)

    def list_all(self):
        return list(self.records.values())