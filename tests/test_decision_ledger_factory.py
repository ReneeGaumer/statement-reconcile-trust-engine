from trust_engine.application.decision_ledger_factory import DecisionLedgerFactory


def test_decision_ledger_factory():
    
    factory = DecisionLedgerFactory()
    entry = factory.create("TR-001")
    
    assert entry.decision_id
    assert entry.trust_record_reference == "TR-001"
    assert entry.rule_version_reference == "TRUST_MODEL_RULES_V1"
    assert entry.decision_timestamp
