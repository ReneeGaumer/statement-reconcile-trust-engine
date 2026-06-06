from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import ExceptionRecordV2

class ExceptionRecordFactory:
    def create(self, severity, penalty, rule_name, source_reference="UNKNOWN_SOURCE", field_name="UNKNOWN_FIELD", original_value="UNKNOWN_ORIGINAL_VALUE", expected_value="UNKNOWN_EXPECTED_VALUE", exception_reason="Exception generated from severity rule evaluation"):
        return ExceptionRecordV2(
            exception_id=str(uuid4()),
            severity=severity,
            penalty=penalty,
            rule_name=rule_name,
            source_reference=source_reference,
            field_name=field_name,
            original_value=original_value,
            expected_value=expected_value,
            exception_reason=exception_reason,
            created_timestamp=datetime.now(UTC)
        )
