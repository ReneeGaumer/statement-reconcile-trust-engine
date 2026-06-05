# Decision Ledger Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

The Decision Ledger is the authoritative record explaining every trust determination made by the system.

It records what decision was made, why it was made, what evidence supported it, what rules were applied, and what exceptions influenced the outcome.

## 2. Authority

The Decision Ledger is authoritative.

Every Trust Record must reference supporting Decision Ledger entries.

## 3. Required Fields

Each Decision Ledger entry must contain:

- decision_id
- decision_timestamp
- decision_type
- decision_outcome
- trust_record_reference
- evidence_references
- deterministic_rule_references
- exception_references
- rationale
- calculation_path_reference
- decision_version
- actor
- created_timestamp

## 4. Decision Requirements

Every decision must be:

- deterministic
- evidence-supported
- reproducible
- auditable

Undocumented assumptions are prohibited.

## 5. Rule Traceability

Every decision must reference:

- rule identifier
- rule version
- rule execution result
- calculation path where applicable

## 6. Evidence Traceability

Every decision must identify the evidence supporting the outcome.

Missing evidence must generate exceptions.

## 7. Exception Influence

Every exception affecting a decision must be recorded and linked.

The ledger must identify how exceptions influenced the outcome.

## 8. Immutability

Finalized Decision Ledger entries are immutable.

Corrections must be recorded as versioned amendments preserving lineage.

## 9. Courtroom Test Requirement

An independent reviewer must be able to reconstruct the exact reasoning path that produced the decision.

## 10. Completion Standard

The Decision Ledger is complete when all decisions, evidence, rules, calculations, and exception influences can be independently reconstructed.

