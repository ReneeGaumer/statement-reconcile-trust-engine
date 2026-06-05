class AuthoritativeRepository:
    def __init__(self, id_field):
        self.id_field = id_field
        self.records = {}

    def save(self, record):
        record_id = getattr(record, self.id_field)
        if record_id in self.records:
            raise ValueError("Authoritative record already exists and cannot be overwritten")
        self.records[record_id] = record
        return record

    def get(self, record_id):
        return self.records.get(record_id)

    def all(self):
        return list(self.records.values())
