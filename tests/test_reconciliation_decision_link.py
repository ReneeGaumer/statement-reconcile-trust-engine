from dataclasses import FrozenInstanceError

import pytest

from trust_engine.reconciliation.reconciliation_decision_link import (
    ReconciliationDecisionLink,
)


def test_reconciliation_decision_link_captures_authoritative_references():
    link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-1",
        decision_explanation_reference="DECISION-EXPLANATION-1",
        reconciliation_record_references=["RECONCILIATION-1", "RECONCILIATION-2"],
        source_document_reference="statement.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )

    assert link.reconciliation_decision_link_id.startswith(
        "RECONCILIATION-DECISION-LINK-"
    )
    assert link.trust_record_reference == "TRUST-1"
    assert link.decision_explanation_reference == "DECISION-EXPLANATION-1"
    assert link.reconciliation_record_references == [
        "RECONCILIATION-1",
        "RECONCILIATION-2",
    ]
    assert link.source_document_reference == "statement.pdf"
    assert link.rule_reference == "RECONCILIATION_RECORD_REFERENCES_CAPTURED"
    assert link.created_timestamp


def test_reconciliation_decision_link_is_immutable():
    link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-1",
        decision_explanation_reference="DECISION-EXPLANATION-1",
        reconciliation_record_references=["RECONCILIATION-1"],
        source_document_reference="statement.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )

    with pytest.raises(FrozenInstanceError):
        link.trust_record_reference = "TRUST-2"


def test_reconciliation_decision_link_defensively_copies_references():
    references = ["RECONCILIATION-1"]

    link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-1",
        decision_explanation_reference="DECISION-EXPLANATION-1",
        reconciliation_record_references=references,
        source_document_reference="statement.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )

    references.append("RECONCILIATION-2")

    assert link.reconciliation_record_references == ["RECONCILIATION-1"]