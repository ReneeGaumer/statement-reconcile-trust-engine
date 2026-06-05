from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory

factory = DecisionLedgerFactory()
entry = factory.create("TR-001")

print(entry)
assert entry.decision_id
assert entry.trust_record_reference == "TR-001"
assert entry.decision_timestamp
print("PASS")
