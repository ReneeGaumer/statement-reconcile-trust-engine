# Reconciliation Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

Reconciliation determines whether records, balances, transactions, and datasets agree according to deterministic reconciliation rules.

## 2. Authority

Reconciliation conclusions are authoritative only when supported by evidence, rules, calculations, and recorded exceptions.

## 3. Required Fields

- reconciliation_id
- reconciliation_version
- source_references
- reconciliation_rule_references
- exception_references
- evidence_references
- result_status
- created_timestamp

## 4. Reconciliation Requirements

Reconciliation must be deterministic, rule-based, evidence-supported, and reproducible.

Unsupported reconciliation adjustments are prohibited.

## 5. Difference Handling

Differences between records must generate reconciliation exceptions until resolved.

## 6. Evidence Requirements

Every reconciliation outcome must reference supporting Evidence Lineage records.

## 7. Courtroom Test Requirement

An independent reviewer must be able to reproduce the reconciliation result using recorded evidence, rules, calculations, and exceptions.

## 8. Completion Standard

A reconciliation result is complete when all inputs, rules, differences, exceptions, and outcomes are independently reproducible.

