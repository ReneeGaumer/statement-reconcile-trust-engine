from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository


class CorrectionAuthorizationRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("correction_authorization_id")