from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class EvidenceLineageRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("lineage_id")
