# Statement Reconcile Trust Engine

A Python Trust Assurance Platform for financial record verification.

The system determines whether sufficient evidence exists to trust a record. It does not assume truth. It evaluates evidence, identifies exceptions, calculates trust, records decisions, and supports audit-ready outputs.

The product is trust, auditability, evidence, reconciliation, exception transparency, and defensible export certification.

## Current Verified Status

- Python package exists under `src/trust_engine/`
- Product governance, specifications, schemas, contracts, workflows, templates, and trust model definitions are tracked in the repository
- Test suite exists under `tests/`
- Verified test command: `python -m pytest`
- Latest verified local result: `26 passed`

## Governing Documents

- Product Constitution: `docs/constitution/CONSTITUTION.md`
- Implementation Roadmap: `docs/roadmap/IMPLEMENTATION_PHASES.md`
- Governance Index: `docs/governance/GOVERNANCE_INDEX.md`
- Specification Index: `docs/specifications/SPECIFICATION_INDEX.md`
- Contract Index: `docs/contracts/CONTRACT_INDEX.md`
- Schema Index: `docs/schemas/SCHEMA_INDEX.md`

## Repository Structure

```text
architecture/data/             Machine-readable governance and trust schemas
docs/constitution/             Product constitution
docs/contracts/                Product contracts for authoritative records
docs/exceptions/               Exception framework documentation
docs/governance/               Change control, governance index, versioning policy
docs/interfaces/               Trust engine and reconciliation interfaces
docs/registries/               Authoritative record and classification registries
docs/roadmap/                  Implementation phase roadmap
docs/schemas/                  Human-readable schema documentation
docs/specifications/           Product and architectural specifications
docs/state-models/             Trust, export, and exception lifecycle models
docs/templates/                Audit, ledger, lineage, and trust record templates
docs/workflows/                Trust determination, reconciliation, and export workflows
src/trust_engine/              Python implementation
tests/                         Pytest test suite
trust-model/classifications/   Trust model and export classification schemas
```

## Implemented Source Areas

```text
src/trust_engine/domain/          Authoritative domain models
src/trust_engine/application/     Trust, evidence, exception, export, and audit factories/evaluators
src/trust_engine/infrastructure/  In-memory repositories and persistence abstractions
src/trust_engine/exceptions/      Exception severity and trust classification support
src/trust_engine/audit/           Audit package namespace
src/trust_engine/rules/           Rule namespace
```

## Authoritative Records

The platform treats these as authoritative records:

- Trust Record
- Evidence Lineage
- Decision Ledger
- Audit Package

Spreadsheets, reports, dashboards, and exports are derived artifacts. They are not the source of truth.

## Export Classifications

Every export must receive exactly one final classification:

- `CLEAN_EXPORT`
- `EXPORT_WITH_WARNINGS`
- `PARTIAL_EXPORT`
- `UNSAFE_EXPORT`
- `EXPORT_EMBARGO`

`EXPORT_EMBARGO` is a hard stop and overrides all other classifications.

## Development

Run the test suite with:

```cmd
python -m pytest
```

Before committing changes:

```cmd
git status
python -m pytest
git diff --stat
```

Commit only intentional changes and keep the working tree clean.

## Core Principle

Trust First. Spreadsheets Second.
