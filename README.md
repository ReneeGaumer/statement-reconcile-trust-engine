# Statement Reconcile Trust Engine

A Python Trust Assurance Platform for financial record verification.

The system determines whether sufficient evidence exists to trust a record. It does not assume truth. It evaluates evidence, identifies exceptions, calculates trust, records decisions, preserves evidence lineage, and supports audit-ready outputs.

The product is trust, auditability, evidence, reconciliation, exception transparency, and defensible export certification.

## Current Verified Status

- Python package exists under `src/trust_engine/`
- Product governance, specifications, schemas, contracts, workflows, templates, and trust model definitions are tracked in the repository
- Test suite exists under `tests/`
- Verified test command: `python -m pytest`
- Latest verified local result: `71 passed`
- Latest verified branch state: `main` clean and synced with `origin/main`

## Current Implemented Assurance Capabilities

- Trust score calculation
- Trust classification
- Evidence lineage record creation and persistence
- Exception record creation and persistence
- Decision explanation creation with required decision path validation
- Decision ledger creation with rationale, evidence references, exception references, rule version, score, classification, outcome, and timestamps
- Audit package creation with reconstruction linkage fields
- Export package creation for export-eligible classifications
- `EXPORT_EMBARGO` hard-stop enforcement
- No export package creation when `EXPORT_EMBARGO` applies
- Authoritative repository overwrite protection
- Defensive-copy protection on repository `save`, `get`, and `all`
- Export reconstruction tests for clean export and embargo paths
- Schema/model alignment checks for core authoritative records

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