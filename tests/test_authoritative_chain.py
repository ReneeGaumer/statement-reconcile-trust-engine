from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity
from tests.governance_test_helpers import (
    authorize_engine_rule_version,
    complete_evidence_lineage_metadata,
)


def test_authoritative_chain_export_embargo():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(
        10,
        [Severity.CRITICAL],
        "statement.pdf",
        evidence_lineage_metadata=complete_evidence_lineage_metadata(),
    )

    lineage = result["evidence_lineage"]
    exceptions = result["exception_records"]
    trust_record = result["trust_record"]
    ledger = result["decision_ledger"]
    audit = result["audit_package"]
    export = result["export_package"]

    assert len(exceptions) == 1
    assert result["embargo"] is True
    assert trust_record.trust_classification == "EXPORT_EMBARGO"
    assert export is None

    assert engine.exception_record_repository.get(exceptions[0].exception_id) == exceptions[0]
    assert engine.evidence_lineage_repository.get(lineage.lineage_id) == lineage
    assert engine.trust_record_repository.get(trust_record.trust_record_id) == trust_record
    assert engine.decision_ledger_repository.get(ledger.decision_id) == ledger
    assert engine.audit_package_repository.get(audit.audit_package_id) == audit