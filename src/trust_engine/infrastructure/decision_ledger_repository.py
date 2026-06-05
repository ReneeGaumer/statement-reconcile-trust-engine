from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class DecisionLedgerRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("decision_id")
