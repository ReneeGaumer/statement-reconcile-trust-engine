from datetime import datetime, UTC

from trust_engine.domain.authoritative_models import RuleVersionRecord
from trust_engine.infrastructure.rule_version_repository import RuleVersionRepository


def test_rule_version_repository_stores_authoritative_rule_version():
    record = RuleVersionRecord(
        rule_version_id="TRUST_MODEL_RULES_V1",
        rule_name="TRUST_MODEL_RULES",
        rule_status="ACTIVE",
        effective_timestamp=datetime.now(UTC),
        rule_fingerprint="TRUST_MODEL_RULES_V1_FINGERPRINT",
        predecessor_version=None,
    )

    repo = RuleVersionRepository()
    repo.save(record)

    loaded = repo.get("TRUST_MODEL_RULES_V1")

    assert loaded == record
    assert loaded.rule_status == "ACTIVE"
    assert loaded.rule_fingerprint == "TRUST_MODEL_RULES_V1_FINGERPRINT"
