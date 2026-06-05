from dataclasses import dataclass

@dataclass(frozen=True)
class ExceptionRecord:
    exception_id: str
    severity: str
    exception_type: str
