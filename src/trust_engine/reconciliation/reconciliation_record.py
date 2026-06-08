from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class ReconciliationRecord:
    reconciliation_id: str
    field_name: str
    expected_value: object
    actual_value: object
    variance: object
    tolerance: object
    status: str
    source_reference: str
    rule_reference: str
    created_timestamp: str

    @classmethod
    def create(
        cls,
        field_name,
        expected_value,
        actual_value,
        variance,
        tolerance,
        status,
        source_reference,
        rule_reference,
    ):
        return cls(
            reconciliation_id="RECONCILIATION-" + str(uuid4()),
            field_name=field_name,
            expected_value=expected_value,
            actual_value=actual_value,
            variance=variance,
            tolerance=tolerance,
            status=status,
            source_reference=source_reference,
            rule_reference=rule_reference,
            created_timestamp=datetime.now(timezone.utc).isoformat(),
        )