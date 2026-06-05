class InMemoryRepository:
    def __init__(self):
        self.records = {}

    def save(self, record_id, record):
        if record_id in self.records:
            raise ValueError("Record already exists and cannot be overwritten")
        self.records[record_id] = record
        return record

    def get(self, record_id):
        return self.records.get(record_id)

    def all(self):
        return list(self.records.values())
