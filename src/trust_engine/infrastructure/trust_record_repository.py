from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class TrustRecordRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("trust_record_id")
