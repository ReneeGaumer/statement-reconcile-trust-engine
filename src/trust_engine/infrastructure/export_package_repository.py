from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class ExportPackageRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("export_package_id")
