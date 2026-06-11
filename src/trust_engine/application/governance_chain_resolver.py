from dataclasses import dataclass

from trust_engine.application.governance_authorization_validator import (
    GovernanceAuthorizationValidator,
)


@dataclass
class GovernanceAuthorizationResult:
    authorized: bool
    rule_version_id: str
    diagnostic_code: str
    diagnostic_message: str


class GovernanceChainResolver:
    AUTHORIZED = "AUTHORIZED"
    MISSING_RULE_VERSION = "MISSING_RULE_VERSION"
    MISSING_RULE_APPROVAL = "MISSING_RULE_APPROVAL"
    MISSING_RULE_GOVERNANCE = "MISSING_RULE_GOVERNANCE"
    INVALID_RULE_GOVERNANCE = "INVALID_RULE_GOVERNANCE"

    def __init__(self, rule_repository, approval_repository, governance_repository):
        self.rule_repository = rule_repository
        self.approval_repository = approval_repository
        self.governance_repository = governance_repository
        self.validator = GovernanceAuthorizationValidator()

    def resolve_authorization(self, rule_version_id):
        rule = self.rule_repository.get(rule_version_id)
        if rule is None:
            return GovernanceAuthorizationResult(
                authorized=False,
                rule_version_id=rule_version_id,
                diagnostic_code=self.MISSING_RULE_VERSION,
                diagnostic_message=(
                    "Rule version is not registered in the authoritative "
                    "rule version repository."
                ),
            )

        approval = next(
            (
                record
                for record in self.approval_repository.all()
                if record.rule_version_reference == rule_version_id
            ),
            None,
        )
        if approval is None:
            return GovernanceAuthorizationResult(
                authorized=False,
                rule_version_id=rule_version_id,
                diagnostic_code=self.MISSING_RULE_APPROVAL,
                diagnostic_message=(
                    "Rule version has no authoritative approval record."
                ),
            )

        governance = next(
            (
                record
                for record in self.governance_repository.all()
                if record.rule_version_reference == rule_version_id
                and record.approval_reference == approval.approval_id
            ),
            None,
        )
        if governance is None:
            return GovernanceAuthorizationResult(
                authorized=False,
                rule_version_id=rule_version_id,
                diagnostic_code=self.MISSING_RULE_GOVERNANCE,
                diagnostic_message=(
                    "Rule version approval has no matching authoritative "
                    "governance authorization record."
                ),
            )

        if not self.validator.is_authorized(rule, approval, governance):
            return GovernanceAuthorizationResult(
                authorized=False,
                rule_version_id=rule_version_id,
                diagnostic_code=self.INVALID_RULE_GOVERNANCE,
                diagnostic_message=(
                    "Rule version governance chain exists but is not authorized."
                ),
            )

        return GovernanceAuthorizationResult(
            authorized=True,
            rule_version_id=rule_version_id,
            diagnostic_code=self.AUTHORIZED,
            diagnostic_message="Rule version governance chain is authorized.",
        )

    def is_rule_authorized(self, rule_version_id):
        return self.resolve_authorization(rule_version_id).authorized