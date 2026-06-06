from trust_engine.application.governance_authorization_validator import GovernanceAuthorizationValidator


class GovernanceChainResolver:
    def __init__(self, rule_repository, approval_repository, governance_repository):
        self.rule_repository = rule_repository
        self.approval_repository = approval_repository
        self.governance_repository = governance_repository
        self.validator = GovernanceAuthorizationValidator()

    def is_rule_authorized(self, rule_version_id):
        rule = self.rule_repository.get(rule_version_id)
        if rule is None:
            return False

        approval = next((record for record in self.approval_repository.all() if record.rule_version_reference == rule_version_id), None)
        if approval is None:
            return False

        governance = next((record for record in self.governance_repository.all() if record.rule_version_reference == rule_version_id and record.approval_reference == approval.approval_id), None)
        if governance is None:
            return False

        return self.validator.is_authorized(rule, approval, governance)
