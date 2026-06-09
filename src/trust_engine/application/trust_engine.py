from trust_engine.application.trust_score_calculator import TrustScoreCalculator
from trust_engine.application.trust_classifier import TrustClassifier
from trust_engine.application.exception_evaluator import ExceptionEvaluator
from trust_engine.application.export_embargo_evaluator import ExportEmbargoEvaluator
from trust_engine.application.trust_record_factory import TrustRecordFactory
from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory
from trust_engine.application.evidence_lineage_factory import EvidenceLineageFactory
from trust_engine.application.audit_package_factory import AuditPackageFactory
from trust_engine.application.exception_record_factory import ExceptionRecordFactory
from trust_engine.application.export_package_factory import ExportPackageFactory
from trust_engine.application.decision_explanation_factory import DecisionExplanationFactory
from trust_engine.application.reconciliation_trust_impact_evaluator import (
    ReconciliationTrustImpactEvaluator,
)
from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.application.governance_chain_resolver import GovernanceChainResolver
from trust_engine.infrastructure.rule_version_repository import RuleVersionRepository
from trust_engine.infrastructure.rule_approval_repository import RuleApprovalRepository
from trust_engine.infrastructure.rule_governance_repository import RuleGovernanceRepository
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository
from trust_engine.infrastructure.decision_ledger_repository import DecisionLedgerRepository
from trust_engine.infrastructure.evidence_lineage_repository import EvidenceLineageRepository
from trust_engine.infrastructure.audit_package_repository import AuditPackageRepository
from trust_engine.infrastructure.exception_record_repository import ExceptionRecordRepository
from trust_engine.infrastructure.export_package_repository import ExportPackageRepository
from trust_engine.infrastructure.decision_explanation_repository import DecisionExplanationRepository
from trust_engine.reconciliation.reconciliation_decision_link import (
    ReconciliationDecisionLink,
)
from trust_engine.reconciliation.reconciliation_decision_link_repository import (
    ReconciliationDecisionLinkRepository,
)
from trust_engine.reconciliation.reconciliation_evaluator import ReconciliationEvaluator
from trust_engine.reconciliation.reconciliation_record_repository import (
    ReconciliationRecordRepository,
)


class TrustEngine:
    def __init__(self):
        self.policy = TrustModelPolicy()
        self.rule_version_repository = RuleVersionRepository()
        self.rule_approval_repository = RuleApprovalRepository()
        self.rule_governance_repository = RuleGovernanceRepository()
        self.governance_chain_resolver = GovernanceChainResolver(
            self.rule_version_repository,
            self.rule_approval_repository,
            self.rule_governance_repository,
        )
        self.score_calculator = TrustScoreCalculator()
        self.classifier = TrustClassifier()
        self.exception_evaluator = ExceptionEvaluator()
        self.embargo_evaluator = ExportEmbargoEvaluator()
        self.record_factory = TrustRecordFactory()
        self.decision_ledger_factory = DecisionLedgerFactory()
        self.evidence_lineage_factory = EvidenceLineageFactory()
        self.audit_package_factory = AuditPackageFactory()
        self.exception_record_factory = ExceptionRecordFactory()
        self.export_package_factory = ExportPackageFactory()
        self.decision_explanation_factory = DecisionExplanationFactory()
        self.trust_record_repository = TrustRecordRepository()
        self.decision_ledger_repository = DecisionLedgerRepository()
        self.evidence_lineage_repository = EvidenceLineageRepository()
        self.audit_package_repository = AuditPackageRepository()
        self.exception_record_repository = ExceptionRecordRepository()
        self.export_package_repository = ExportPackageRepository()
        self.decision_explanation_repository = DecisionExplanationRepository()
        self.reconciliation_evaluator = ReconciliationEvaluator()
        self.reconciliation_trust_impact_evaluator = (
            ReconciliationTrustImpactEvaluator(self.policy)
        )
        self.reconciliation_record_repository = ReconciliationRecordRepository()
        self.reconciliation_decision_link_repository = (
            ReconciliationDecisionLinkRepository()
        )

    def determine_trust(self, evidence_count, severities, source_document_reference, prebuilt_exception_records=None):
        rule_version_reference = self.policy.RULE_VERSION_REFERENCE
        if not self.governance_chain_resolver.is_rule_authorized(rule_version_reference):
            raise PermissionError(
                f"unauthorized rule version: {rule_version_reference}"
            )

        evidence_lineage = self.evidence_lineage_factory.create(source_document_reference)
        exception_records = list(prebuilt_exception_records or [])

        for severity in severities:
            penalty = self.exception_evaluator.penalty(severity)
            exception_record = self.exception_record_factory.create(
                severity.value,
                penalty,
                self.policy.EXCEPTION_PENALTY_RULE,
                source_reference=source_document_reference,
                field_name="TRUST_SEVERITY",
                original_value=severity.value,
                expected_value="NO_EXCEPTION",
                exception_reason=severity.name + " severity triggered trust exception",
            )
            self.exception_record_repository.save(exception_record)
            exception_records.append(exception_record)

        total_penalty = sum(record.penalty for record in exception_records)
        embargo = self.embargo_evaluator.should_embargo(severities)
        score = self.score_calculator.calculate(evidence_count, total_penalty)
        classification = self.classifier.classify(score, embargo)

        trust_record = self.record_factory.create(
            score,
            classification.value,
            evidence_count=evidence_count,
            exception_count=len(exception_records),
            exception_penalty=total_penalty,
            embargo=embargo,
            trust_calculation_rule=self.policy.SCORE_CALCULATION_RULE,
            evidence_lineage_reference=evidence_lineage.lineage_id,
            exception_record_references=[
                record.exception_id for record in exception_records
            ],
        )

        decision_path = [
            {
                "step": "EVIDENCE_LINEAGE_CREATED",
                "rule": "SOURCE_DOCUMENT_REFERENCE_CAPTURED",
                "inputs": {"source_document_reference": source_document_reference},
                "output": evidence_lineage.lineage_id,
            },
            {
                "step": "TRUST_POLICY_SOURCE_LOADED",
                "rule": "TRUST_MODEL_POLICY_SOURCE_METADATA_CAPTURED",
                "inputs": {},
                "output": self.policy.policy_source_metadata(),
            },
            {
                "step": "EXCEPTION_RULES_EVALUATED",
                "rule": self.policy.EXCEPTION_PENALTY_RULE,
                "inputs": {"severities": [severity.value for severity in severities]},
                "output": {
                    "exception_count": len(exception_records),
                    "exception_penalty": total_penalty,
                    "exception_record_references": [
                        record.exception_id for record in exception_records
                    ],
                },
            },
            {
                "step": "TRUST_SCORE_CALCULATED",
                "rule": self.policy.SCORE_CALCULATION_RULE,
                "inputs": {
                    "evidence_count": evidence_count,
                    "exception_penalty": total_penalty,
                },
                "output": score,
            },
            {
                "step": "EXPORT_EMBARGO_EVALUATED",
                "rule": self.policy.EMBARGO_RULE,
                "inputs": {"severities": [severity.value for severity in severities]},
                "output": embargo,
            },
            {
                "step": "TRUST_CLASSIFICATION_ASSIGNED",
                "rule": self.policy.CLASSIFICATION_RULE,
                "inputs": {"trust_score": score, "embargo": embargo},
                "output": classification.value,
            },
        ]

        decision_explanation = self.decision_explanation_factory.create(
            trust_record.trust_record_id,
            evidence_count,
            len(exception_records),
            total_penalty,
            embargo,
            score,
            classification.value,
            decision_path,
            [record.exception_id for record in exception_records],
        )

        decision_ledger = self.decision_ledger_factory.create(
            trust_record_reference=trust_record.trust_record_id,
            decision_explanation_reference=decision_explanation.decision_explanation_id,
            rule_version_reference=rule_version_reference,
            decision_rationale=(
                "Trust classification derived from evidence lineage, exception "
                "evaluation, trust score calculation, and embargo evaluation."
            ),
            evidence_references=[evidence_lineage.lineage_id],
            exception_references=[record.exception_id for record in exception_records],
            trust_score=score,
            trust_classification=classification.value,
            decision_outcome=classification.value,
        )

        audit_package = self.audit_package_factory.create(
            trust_record.trust_record_id,
            evidence_lineage.lineage_id,
            decision_ledger.decision_id,
            decision_explanation.decision_explanation_id,
            [rule_version_reference],
            [record.exception_id for record in exception_records],
            score,
            classification.value,
            classification.value,
        )

        self.evidence_lineage_repository.save(evidence_lineage)
        self.trust_record_repository.save(trust_record)
        self.decision_ledger_repository.save(decision_ledger)
        self.decision_explanation_repository.save(decision_explanation)
        self.audit_package_repository.save(audit_package)

        export_package = None
        if classification.value != "EXPORT_EMBARGO":
            export_package = self.export_package_factory.create(
                trust_record.trust_record_id,
                audit_package.audit_package_id,
                classification.value,
            )
            self.export_package_repository.save(export_package)

        return {
            "evidence_lineage": evidence_lineage,
            "exception_records": exception_records,
            "trust_record": trust_record,
            "decision_ledger": decision_ledger,
            "decision_explanation": decision_explanation,
            "audit_package": audit_package,
            "export_package": export_package,
            "embargo": embargo,
            "exception_penalty": total_penalty,
        }

    def determine_trust_with_reconciliation(
        self,
        evidence_count,
        severities,
        source_document_reference,
        reconciliation_inputs,
    ):
        reconciliation_records = []

        for reconciliation_input in reconciliation_inputs:
            reconciliation_record = self.reconciliation_evaluator.evaluate(
                field_name=reconciliation_input["field_name"],
                expected_value=reconciliation_input.get("expected_value"),
                actual_value=reconciliation_input.get("actual_value"),
                tolerance=reconciliation_input.get("tolerance", 0),
                source_reference=source_document_reference,
            )
            self.reconciliation_record_repository.save(reconciliation_record)
            reconciliation_records.append(reconciliation_record)

        reconciliation_exception_records = []
        trust_impact_statuses = self.policy.reconciliation_trust_impact_statuses()
        trust_impact_severity = self.policy.reconciliation_trust_impact_severity()

        for reconciliation_record in reconciliation_records:
            if reconciliation_record.status in trust_impact_statuses:
                penalty = self.exception_evaluator.penalty(trust_impact_severity)
                exception_record = self.exception_record_factory.create(
                    trust_impact_severity.value,
                    penalty,
                    self.policy.RECONCILIATION_TRUST_IMPACT_RULE,
                    source_reference=reconciliation_record.reconciliation_id,
                    field_name=reconciliation_record.field_name,
                    original_value=reconciliation_record.actual_value,
                    expected_value=reconciliation_record.expected_value,
                    exception_reason=(
                        reconciliation_record.status
                        + " reconciliation status triggered trust exception for field "
                        + reconciliation_record.field_name
                    ),
                )
                self.exception_record_repository.save(exception_record)
                reconciliation_exception_records.append(exception_record)

        reconciliation_exception_severities = [
            trust_impact_severity for _ in reconciliation_exception_records
        ]

        result = self.determine_trust(
            evidence_count,
            list(severities),
            source_document_reference,
            prebuilt_exception_records=reconciliation_exception_records,
        )

        reconciliation_record_references = [
            record.reconciliation_id for record in reconciliation_records
        ]

        reconciliation_decision_link = ReconciliationDecisionLink.create(
            trust_record_reference=result["trust_record"].trust_record_id,
            decision_explanation_reference=result[
                "decision_explanation"
            ].decision_explanation_id,
            reconciliation_record_references=reconciliation_record_references,
            source_document_reference=source_document_reference,
            rule_reference=self.policy.RECONCILIATION_TRUST_IMPACT_RULE,
        )
        self.reconciliation_decision_link_repository.save(
            reconciliation_decision_link
        )

        result["reconciliation_records"] = reconciliation_records
        result["reconciliation_record_references"] = reconciliation_record_references
        result["reconciliation_decision_link"] = reconciliation_decision_link
        result["reconciliation_decision_link_reference"] = (
            reconciliation_decision_link.reconciliation_decision_link_id
        )

        return result