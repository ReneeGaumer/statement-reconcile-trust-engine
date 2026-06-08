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
from trust_engine.application.trust_model_policy import TrustModelPolicy
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository
from trust_engine.infrastructure.decision_ledger_repository import DecisionLedgerRepository
from trust_engine.infrastructure.evidence_lineage_repository import EvidenceLineageRepository
from trust_engine.infrastructure.audit_package_repository import AuditPackageRepository
from trust_engine.infrastructure.exception_record_repository import ExceptionRecordRepository
from trust_engine.infrastructure.export_package_repository import ExportPackageRepository
from trust_engine.infrastructure.decision_explanation_repository import DecisionExplanationRepository


class TrustEngine:
    def __init__(self):
        self.policy = TrustModelPolicy()
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

    def determine_trust(self, evidence_count, severities, source_document_reference):
        evidence_lineage = self.evidence_lineage_factory.create(source_document_reference)
        exception_records = []

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
            exception_record_references=[record.exception_id for record in exception_records],
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

        rule_version_reference = self.policy.RULE_VERSION_REFERENCE
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