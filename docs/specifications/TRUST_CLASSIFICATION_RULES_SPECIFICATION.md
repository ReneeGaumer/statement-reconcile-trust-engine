# Trust Classification Rules Specification

Status: AUTHORITATIVE SPECIFICATION
Version: 1.0.0
Constitution Reference: docs\constitution\CONSTITUTION.md
Effective Date: 2026-06-05

## 1. Purpose

Defines assignment rules for final trust classifications.

## 2. Allowed Classifications

- CLEAN_EXPORT
- EXPORT_WITH_WARNINGS
- PARTIAL_EXPORT
- UNSAFE_EXPORT
- EXPORT_EMBARGO

## 3. Rule Requirements

Classification assignment must be deterministic, evidence-supported, exception-sensitive, and reproducible.

## 4. Embargo Supremacy

EXPORT_EMBARGO overrides all other classifications.

## 5. Courtroom Test Requirement

An independent reviewer must be able to explain exactly why the classification was assigned.

## 6. Completion Standard

Classification logic is complete when the same inputs always produce the same classification.
