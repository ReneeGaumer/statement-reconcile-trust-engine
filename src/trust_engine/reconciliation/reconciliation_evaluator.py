from decimal import Decimal, InvalidOperation

from trust_engine.reconciliation.reconciliation_record import ReconciliationRecord
from trust_engine.reconciliation.reconciliation_status import ReconciliationStatus


class ReconciliationEvaluator:
    EXACT_AMOUNT_MATCH_RULE = "EXACT_AMOUNT_MATCH"
    TOLERANCE_AMOUNT_MATCH_RULE = "TOLERANCE_AMOUNT_MATCH"
    MISSING_EXPECTED_RULE = "MISSING_EXPECTED_VALUE"
    MISSING_ACTUAL_RULE = "MISSING_ACTUAL_VALUE"
    UNRECONCILABLE_RULE = "UNRECONCILABLE_VALUE_COMPARISON"

    def evaluate(
        self,
        field_name,
        expected_value,
        actual_value,
        source_reference,
        tolerance=0,
    ):
        if expected_value is None:
            return ReconciliationRecord.create(
                field_name=field_name,
                expected_value=expected_value,
                actual_value=actual_value,
                variance=None,
                tolerance=tolerance,
                status=ReconciliationStatus.MISSING_EXPECTED.value,
                source_reference=source_reference,
                rule_reference=self.MISSING_EXPECTED_RULE,
            )

        if actual_value is None:
            return ReconciliationRecord.create(
                field_name=field_name,
                expected_value=expected_value,
                actual_value=actual_value,
                variance=None,
                tolerance=tolerance,
                status=ReconciliationStatus.MISSING_ACTUAL.value,
                source_reference=source_reference,
                rule_reference=self.MISSING_ACTUAL_RULE,
            )

        try:
            expected_decimal = Decimal(str(expected_value))
            actual_decimal = Decimal(str(actual_value))
            tolerance_decimal = abs(Decimal(str(tolerance)))
        except (InvalidOperation, ValueError):
            return ReconciliationRecord.create(
                field_name=field_name,
                expected_value=expected_value,
                actual_value=actual_value,
                variance=None,
                tolerance=tolerance,
                status=ReconciliationStatus.UNRECONCILABLE.value,
                source_reference=source_reference,
                rule_reference=self.UNRECONCILABLE_RULE,
            )

        variance = actual_decimal - expected_decimal

        if variance == Decimal("0"):
            status = ReconciliationStatus.MATCH.value
            rule_reference = self.EXACT_AMOUNT_MATCH_RULE
        elif abs(variance) <= tolerance_decimal:
            status = ReconciliationStatus.MATCH_WITH_TOLERANCE.value
            rule_reference = self.TOLERANCE_AMOUNT_MATCH_RULE
        else:
            status = ReconciliationStatus.MISMATCH.value
            rule_reference = self.EXACT_AMOUNT_MATCH_RULE

        return ReconciliationRecord.create(
            field_name=field_name,
            expected_value=expected_value,
            actual_value=actual_value,
            variance=variance,
            tolerance=tolerance_decimal,
            status=status,
            source_reference=source_reference,
            rule_reference=rule_reference,
        )