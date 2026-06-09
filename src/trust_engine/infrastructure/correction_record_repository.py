from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class CorrectionRecordRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("correction_id")