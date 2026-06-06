from datetime import datetime, UTC

from trust_engine.domain.authoritative_models import RuleVersionRecord
from trust_engine.infrastructure.authoritative_repository import AuthoritativeRepository


def test_rule_version_repository_stores_authoritative_rule_version():
    record = RuleVersionRecord(
        rule_version_id="TRUST_MODEL_RULES_V1",
        rule_name="TRUST_MODEL_RULES",
        rule_status="ACTIVE",
        effective_timestamp=datetime.now(UTC),
        rule_fingerprint="TRUST_MODEL_RULES_V1_FINGERPRINT",
        predecessor_version=None,
    )

    repo = AuthoritativeRepository("rule_version_id")
    repo.save(record)

    loaded = repo.get("TRUST_MODEL_RULES_V1")

    assert loaded == record
    assert loaded.rule_status == "ACTIVE"
    assert loaded.rule_fingerprint == "TRUST_MODEL_RULES_V1_FINGERPRINT"
