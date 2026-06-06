from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository

class DecisionExplanationRepository(AuthoritativeRepository):
    def __init__(self):
        super().__init__("decision_explanation_id")
