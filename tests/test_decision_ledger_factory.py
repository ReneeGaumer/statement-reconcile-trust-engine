from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory


def test_decision_ledger_factory():
    
    factory = DecisionLedgerFactory()
    entry = factory.create("TR-001")
    
    assert entry.decision_id
    assert entry.trust_record_reference == "TR-001"
    assert entry.decision_timestamp
