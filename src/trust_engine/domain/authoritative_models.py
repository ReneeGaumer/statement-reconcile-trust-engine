from dataclasses import dataclass
from datetime import datetime

@dataclass
class TrustRecord:
    trust_record_id:str
    trust_score:float
    trust_classification:str
    evidence_count:int
    exception_count:int
    exception_penalty:float
    embargo:bool
    trust_calculation_rule:str
    evidence_lineage_reference:str
    exception_record_references:list
    created_timestamp:datetime

@dataclass
class DecisionLedgerEntry:
    decision_id: str
    trust_record_reference: str
    decision_explanation_reference: str
    rule_version_reference: str
    decision_rationale: str
    evidence_references: list
    exception_references: list
    trust_score: float
    trust_classification: str
    decision_outcome: str
    decision_timestamp: datetime
    created_timestamp: datetime

@dataclass
class DecisionExplanationRecord:
    decision_explanation_id:str
    trust_record_reference:str
    evidence_count:int
    exception_count:int
    exception_penalty:float
    embargo:bool
    trust_score:float
    trust_classification:str
    exception_record_references:list
    decision_path:list
    created_timestamp:datetime

@dataclass
class EvidenceLineageRecord:
    lineage_id: str
    lineage_version: str
    source_document_reference: str
    source_location: str
    page_reference: str
    acquisition_method: str
    acquisition_timestamp: datetime
    evidence_hash: str
    chain_of_custody: list
    evidence_type: str
    evidence_status: str
    created_timestamp: datetime

@dataclass
class ExceptionRecord:
    exception_id:str
    severity:str
    created_timestamp:datetime


@dataclass
class AuditPackage:
    audit_package_id: str
    trust_record_reference: str
    evidence_lineage_reference: str
    decision_ledger_reference: str
    decision_explanation_reference: str
    rule_version_references: list
    exception_references: list
    trust_score: float
    trust_classification: str
    export_classification: str
    reconstruction_status: str
    audit_package_status: str
    created_timestamp: datetime


@dataclass
class ExceptionRecordV2:
    exception_id:str
    severity:str
    penalty:float
    rule_name:str
    source_reference:str
    field_name:str
    original_value:str
    expected_value:str
    exception_reason:str
    remediation_guidance:str
    status:str
    active:bool
    created_timestamp:datetime


@dataclass
class CorrectionRecord:
    correction_id:str
    original_value:str
    corrected_value:str
    correction_reason:str
    correction_timestamp:datetime
    correction_authorization_reference:str
    evidence_reference:str
    exception_reference:str


@dataclass
class CorrectionAuthorizationRecord:
    correction_authorization_id:str
    correction_id_reference:str
    authorized_by:str
    authorization_timestamp:datetime
    authorization_status:str
    authorization_reason:str


@dataclass
class ExportPackage:
    export_package_id:str
    trust_record_reference:str
    audit_package_reference:str
    export_classification:str
    created_timestamp:datetime


@dataclass
class RuleVersionRecord:
    rule_version_id:str
    rule_name:str
    rule_status:str
    effective_timestamp:datetime
    rule_fingerprint:str
    predecessor_version:str


@dataclass
class RuleApprovalRecord:
    approval_id:str
    rule_version_reference:str
    approver:str
    approval_timestamp:datetime
    approval_status:str


@dataclass
class RuleGovernanceRecord:
    governance_id:str
    rule_version_reference:str
    approval_reference:str
    governance_status:str
    effective_timestamp:datetime
    authorized_by:str
    governance_reason:str
