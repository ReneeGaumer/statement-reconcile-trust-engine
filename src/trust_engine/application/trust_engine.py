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
from trust_engine.infrastructure.trust_record_repository import TrustRecordRepository
from trust_engine.infrastructure.decision_ledger_repository import DecisionLedgerRepository
from trust_engine.infrastructure.evidence_lineage_repository import EvidenceLineageRepository
from trust_engine.infrastructure.audit_package_repository import AuditPackageRepository
from trust_engine.infrastructure.exception_record_repository import ExceptionRecordRepository
from trust_engine.infrastructure.export_package_repository import ExportPackageRepository
from trust_engine.infrastructure.decision_explanation_repository import DecisionExplanationRepository

class TrustEngine:
    def __init__(self):
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
            exception_record = self.exception_record_factory.create(severity.value, penalty, severity.name + "_EXCEPTION_RULE")
            self.exception_record_repository.save(exception_record)
            exception_records.append(exception_record)
        total_penalty = sum(record.penalty for record in exception_records)
        embargo = self.embargo_evaluator.should_embargo(severities)
        score = self.score_calculator.calculate(evidence_count, total_penalty)
        classification = self.classifier.classify(score, embargo)
        trust_record = self.record_factory.create(score, classification.value)
        decision_ledger = self.decision_ledger_factory.create(trust_record.trust_record_id)
        decision_explanation = self.decision_explanation_factory.create(trust_record.trust_record_id, evidence_count, len(exception_records), total_penalty, embargo, score, classification.value)
        audit_package = self.audit_package_factory.create(trust_record.trust_record_id, evidence_lineage.lineage_id, decision_ledger.decision_id)
        self.evidence_lineage_repository.save(evidence_lineage)
        self.trust_record_repository.save(trust_record)
        self.decision_ledger_repository.save(decision_ledger)
        self.decision_explanation_repository.save(decision_explanation)
        self.audit_package_repository.save(audit_package)
        export_package = self.export_package_factory.create(trust_record.trust_record_id, audit_package.audit_package_id, classification.value)
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
            "exception_penalty": total_penalty
        }
