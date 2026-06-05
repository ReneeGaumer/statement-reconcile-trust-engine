# Data Preservation Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

This specification governs preservation of original values, corrected values, correction rationale, timestamps, and correction lineage.

## 2. Original Value Immutability

Original values are immutable and must never be overwritten.

## 3. Correction Requirements

Every correction must preserve:

- original_value
- corrected_value
- correction_reason
- correction_timestamp
- correction_authorization_reference
- evidence_reference
- exception_reference

## 4. Prohibited Actions

Silent correction is prohibited.

Deletion of authoritative correction history is prohibited.

## 5. Courtroom Test Requirement

An independent reviewer must be able to reconstruct the original value, corrected value, correction reason, evidence, and authorization path.

## 6. Completion Standard

Correction lineage is complete when every correction can be independently reconstructed and defended.
