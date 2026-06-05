# Evidence Lineage Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

Evidence Lineage is the authoritative record describing the complete evidence chain supporting a trust determination.

Its purpose is to allow independent reconstruction of every conclusion contained within a Trust Record, Decision Ledger, or Audit Package.

## 2. Authority

Evidence Lineage is an authoritative record.

Derived artifacts may reference Evidence Lineage but may not replace it.

## 3. Required Fields

Each Evidence Lineage record must contain:

- lineage_id
- lineage_version
- source_document_reference
- source_location
- page_reference
- acquisition_method
- acquisition_timestamp
- evidence_hash
- chain_of_custody
- evidence_type
- evidence_status
- trust_record_references
- decision_ledger_references
- audit_package_references
- created_timestamp

## 4. Evidence Requirements

Every evidence item must be:

- traceable
- reproducible
- auditable
- attributable

Evidence may not be fabricated, synthesized, assumed, or altered without recorded correction lineage.

## 5. Chain of Custody

Evidence Lineage must preserve:

- acquisition source
- acquisition timestamp
- transformation history
- storage location history
- access history where available

## 6. Courtroom Test Requirement

An independent reviewer must be able to identify the exact source and path used to support a conclusion.

If evidence cannot be traced, an exception must be generated.

## 7. Completion Standard

Evidence Lineage is complete when every trust determination can be traced back to verifiable source evidence without undocumented assumptions.

