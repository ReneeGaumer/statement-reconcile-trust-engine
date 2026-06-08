from copy import deepcopy


class AuthoritativeRepository:
    def __init__(self, id_field):
        self.id_field = id_field
        self.records = {}

    def save(self, record):
        record_id = getattr(record, self.id_field)
        if record_id in self.records:
            raise ValueError("Authoritative record already exists and cannot be overwritten")
        self.records[record_id] = deepcopy(record)
        return deepcopy(self.records[record_id])

    def get(self, record_id):
        record = self.records.get(record_id)
        if record is None:
            return None
        return deepcopy(record)

    def all(self):
        return deepcopy(list(self.records.values()))