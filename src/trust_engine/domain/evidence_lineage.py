from dataclasses import dataclass

@dataclass(frozen=True)
class EvidenceLineage:
    lineage_id: str
    evidence_hash: str
    source_reference: str
