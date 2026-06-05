# Export Embargo Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

Export Embargo prevents release of outputs when trust conditions fail.

## 2. Authority

EXPORT_EMBARGO is a mandatory hard stop.

## 3. Embargo Triggers

- insufficient evidence
- unreconstructable trust determination
- unresolved critical exception
- missing audit package
- missing decision ledger linkage
- invalid trust score calculation
- failed courtroom test

## 4. Required Fields

- embargo_id
- embargo_reason
- triggering_exception_references
- trust_record_reference
- decision_ledger_reference
- timestamp

## 5. Override Rule

EXPORT_EMBARGO overrides all other export classifications.

## 6. Completion Standard

Embargo records are complete when the triggering conditions and supporting evidence are independently reconstructible.
