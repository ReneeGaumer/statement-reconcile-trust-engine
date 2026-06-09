from datetime import UTC, datetime

from trust_engine.domain.authoritative_models import (
    CorrectionAuthorizationRecord,
)
from trust_engine.infrastructure.correction_authorization_repository import (
    CorrectionAuthorizationRepository,
)


def build_authorization():
    return CorrectionAuthorizationRecord(
        correction_authorization_id="AUTH-001",
        correction_id_reference="CORR-001",
        authorization_status="AUTHORIZED",
        authorized_by="GOVERNANCE_AUTHORITY",
        authorization_timestamp=datetime.now(UTC),
        authorization_reason="Authorized correction.",
    )


def test_correction_authorization_repository_stores_authoritative_record():
    record = build_authorization()
    repo = CorrectionAuthorizationRepository()

    repo.save(record)

    loaded = repo.get("AUTH-001")

    assert loaded == record
    assert loaded.authorization_status == "AUTHORIZED"
    assert loaded.authorized_by == "GOVERNANCE_AUTHORITY"


def test_correction_authorization_repository_is_append_only():
    record = build_authorization()
    repo = CorrectionAuthorizationRepository()

    repo.save(record)

    try:
        repo.save(record)
        raise AssertionError("overwrite should have failed")
    except ValueError:
        pass


def test_correction_authorization_repository_returns_defensive_copies():
    record = build_authorization()
    repo = CorrectionAuthorizationRepository()

    repo.save(record)

    loaded = repo.get("AUTH-001")
    loaded.authorization_status = "REVOKED"

    loaded_again = repo.get("AUTH-001")

    assert loaded_again.authorization_status == "AUTHORIZED"