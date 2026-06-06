class GovernanceAuthorizationValidator:
    def is_authorized(self, rule, approval, governance):
        if rule.rule_status != "ACTIVE":
            return False
        if approval.approval_status != "APPROVED":
            return False
        if governance.governance_status != "AUTHORIZED":
            return False
        if approval.rule_version_reference != rule.rule_version_id:
            return False
        if governance.rule_version_reference != rule.rule_version_id:
            return False
        if governance.approval_reference != approval.approval_id:
            return False
        return True
