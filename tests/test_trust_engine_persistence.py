from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity

engine = TrustEngine()
result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

lineage = result["evidence_lineage"]
record = result["trust_record"]
ledger = result["decision_ledger"]
audit = result["audit_package"]

assert engine.evidence_lineage_repository.get(lineage.lineage_id) == lineage
assert engine.trust_record_repository.get(record.trust_record_id) == record
assert engine.decision_ledger_repository.get(ledger.decision_id) == ledger
assert engine.audit_package_repository.get(audit.audit_package_id) == audit

assert audit.trust_record_reference == record.trust_record_id
assert audit.evidence_lineage_reference == lineage.lineage_id
assert audit.decision_ledger_reference == ledger.decision_id
assert ledger.trust_record_reference == record.trust_record_id
assert record.trust_classification == "EXPORT_EMBARGO"

print(lineage)
print(record)
print(ledger)
print(audit)
print("PASS")
