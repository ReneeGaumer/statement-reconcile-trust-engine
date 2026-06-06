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
    decision_id:str
    trust_record_reference:str
    decision_explanation_reference:str
    decision_timestamp:datetime

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
    decision_path:list
    created_timestamp:datetime

@dataclass
class EvidenceLineageRecord:
    lineage_id:str
    source_document_reference:str
    acquisition_timestamp:datetime

@dataclass
class ExceptionRecord:
    exception_id:str
    severity:str
    created_timestamp:datetime


@dataclass
class AuditPackage:
    audit_package_id:str
    trust_record_reference:str
    evidence_lineage_reference:str
    decision_ledger_reference:str
    decision_explanation_reference:str
    created_timestamp:datetime


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
    created_timestamp:datetime


@dataclass
class ExportPackage:
    export_package_id:str
    trust_record_reference:str
    audit_package_reference:str
    export_classification:str
    created_timestamp:datetime
