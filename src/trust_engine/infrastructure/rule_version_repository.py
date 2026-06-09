from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository


class RuleVersionRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("rule_version_id")