# Export Classification Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

Export Classification determines whether a derived export is eligible for release and under what trust condition.

## 2. Authority

Export classifications are authoritative trust outcomes and must be recorded in the Decision Ledger and Audit Package.

## 3. Classification Values

Exactly one final classification must be assigned:

- CLEAN_EXPORT
- EXPORT_WITH_WARNINGS
- PARTIAL_EXPORT
- UNSAFE_EXPORT
- EXPORT_EMBARGO

EXPORT_EMBARGO is a hard stop and overrides all other classifications.

## 4. Required Inputs

- trust_record_reference
- trust_score_reference
- evidence_lineage_references
- decision_ledger_references
- exception_references
- audit_package_reference
- export_eligibility_rules
- classification_timestamp

## 5. Classification Requirements

Export classification must be deterministic, evidence-supported, exception-sensitive, and reproducible.

Unsupported export certification is prohibited.

## 6. Embargo Requirements

EXPORT_EMBARGO must prevent export generation or release.

Embargo conditions override score-based classifications.

## 7. Courtroom Test Requirement

An independent reviewer must be able to reconstruct why the export classification was assigned.

## 8. Completion Standard

Export classification is complete when the classification, rule path, evidence, exceptions, score, and audit references are fully reconstructible.

