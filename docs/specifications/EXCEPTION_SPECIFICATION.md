# Exception Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

Exceptions are authoritative records describing conditions that reduce trust, prevent trust determination, or require reviewer attention.

## 2. Authority

Exceptions are authoritative records and must never be silently suppressed.

## 3. Required Fields

- exception_id
- exception_type
- severity
- status
- source_reference
- evidence_reference
- trust_impact
- remediation_guidance
- created_timestamp
- resolved_timestamp
- resolution_reference

## 4. Severity Levels

Exceptions must be classified using deterministic severity levels.

Severity must be evidence-supported and reproducible.

## 5. Lifecycle

Exception lifecycle states:

- OPEN
- RESOLVED
- CLOSED

Status transitions must be recorded.

## 6. Trust Impact

Every exception must explicitly document trust impact.

Trust impact must influence trust classification where applicable.

## 7. Evidence Requirements

Every exception must reference supporting evidence.

Unsupported exceptions are prohibited.

## 8. Remediation Requirements

Exceptions should include remediation guidance when remediation is possible.

## 9. Courtroom Test Requirement

An independent reviewer must be able to understand why the exception exists and how it influenced trust outcomes.

## 10. Completion Standard

An exception record is complete when cause, evidence, impact, status, and resolution state are fully documented.

