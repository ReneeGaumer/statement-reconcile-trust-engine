from trust_engine.application.trust_engine import TrustEngine
from trust_engine.exceptions.severity import Severity
from tests.governance_test_helpers import authorize_engine_rule_version


def test_trust_engine_end_to_end_clean_export():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [], "statement.pdf")

    assert result["trust_record"].trust_classification == "CLEAN_EXPORT"
    assert result["export_package"] is not None


def test_trust_engine_end_to_end_export_embargo():
    engine = TrustEngine()
    authorize_engine_rule_version(engine)

    result = engine.determine_trust(10, [Severity.CRITICAL], "statement.pdf")

    assert result["trust_record"].trust_classification == "EXPORT_EMBARGO"
    assert result["export_package"] is None