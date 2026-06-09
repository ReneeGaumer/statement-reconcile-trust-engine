from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository


class RuleApprovalRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("approval_id")