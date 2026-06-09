from datetime import UTC, datetime

import pytest

from trust_engine.application.correction_record_validator import (
    CorrectionRecordValidator,
)
from trust_engine.domain.authoritative_models import CorrectionRecord


def valid_record():
    return CorrectionRecord(
        correction_id="CORR-1",
        original_value="100",
        corrected_value="200",
        correction_reason="Documented correction",
        correction_timestamp=datetime.now(UTC),
        correction_authorization_reference="AUTH-1",
        evidence_reference="EVID-1",
        exception_reference="EXC-1",
    )


def test_valid_correction_record_passes_validation():
    validator = CorrectionRecordValidator()

    assert validator.validate(valid_record()) is True


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        ("correction_id", ""),
        ("original_value", ""),
        ("corrected_value", ""),
        ("correction_reason", ""),
        ("correction_timestamp", None),
        ("correction_authorization_reference", ""),
        ("evidence_reference", ""),
        ("exception_reference", ""),
    ],
)
def test_missing_required_field_raises_value_error(
    field_name,
    replacement,
):
    validator = CorrectionRecordValidator()

    record = valid_record()
    setattr(record, field_name, replacement)

    with pytest.raises(ValueError, match=f"{field_name} is required"):
        validator.validate(record)