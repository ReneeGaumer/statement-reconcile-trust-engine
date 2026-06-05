from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class AuditPackageRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("audit_package_id")
