from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository


class RuleGovernanceRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("governance_id")