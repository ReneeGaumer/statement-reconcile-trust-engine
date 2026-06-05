from datetime import datetime, UTC
from uuid import uuid4
from trust_engine.domain.authoritative_models import ExceptionRecordV2

class ExceptionRecordFactory:
    def create(self, severity, penalty, rule_name):
        return ExceptionRecordV2(
            exception_id=str(uuid4()),
            severity=severity,
            penalty=penalty,
            rule_name=rule_name,
            created_timestamp=datetime.now(UTC)
        )
