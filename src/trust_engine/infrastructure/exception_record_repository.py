from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class ExceptionRecordRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("exception_id")
