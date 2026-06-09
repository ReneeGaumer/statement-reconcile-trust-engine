class CorrectionRecordValidator:
    REQUIRED_FIELDS = (
        "correction_id",
        "original_value",
        "corrected_value",
        "correction_reason",
        "correction_timestamp",
        "correction_authorization_reference",
        "evidence_reference",
        "exception_reference",
    )

    def validate(self, correction_record):
        for field_name in self.REQUIRED_FIELDS:
            value = getattr(correction_record, field_name)

            if value is None:
                raise ValueError(f"{field_name} is required")

            if isinstance(value, str) and value.strip() == "":
                raise ValueError(f"{field_name} is required")

        return True