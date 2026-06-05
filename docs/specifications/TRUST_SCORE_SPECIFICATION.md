# Trust Score Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

The Trust Score provides a deterministic quantitative representation of trust supported by available evidence and affected by recorded exceptions.

## 2. Authority

Trust Scores are authoritative only when supported by evidence, rules, calculations, and references recorded within authoritative records.

## 3. Required Fields

- trust_score
- score_version
- calculation_reference
- trust_record_reference
- evidence_references
- exception_references
- rule_references
- calculation_timestamp

## 4. Deterministic Calculation Requirements

Trust scores must be deterministic, reproducible, and evidence-derived.

Manual trust score override is prohibited.

All score inputs must be traceable to authoritative records.

## 5. Evidence Requirements

Trust score calculations must reference supporting Evidence Lineage records.

Missing evidence must reduce trust through deterministic rules or generate exceptions.

## 6. Exception Sensitivity

Active exceptions must influence trust scores through deterministic rule application.

Exception impact must be explainable and reproducible.


## 7. Rule Requirements

Every trust score must reference the exact rule version used during calculation.

## 8. Courtroom Test Requirement

An independent reviewer must be able to reproduce the score using recorded evidence, rules, and exceptions.

## 9. Completion Standard

A Trust Score is complete when calculation inputs, outputs, rules, evidence, and exception influences are independently reproducible.

