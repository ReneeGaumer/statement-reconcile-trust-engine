import pytest

from trust_engine.reconciliation.reconciliation_decision_link import (
    ReconciliationDecisionLink,
)
from trust_engine.reconciliation.reconciliation_decision_link_repository import (
    ReconciliationDecisionLinkRepository,
)


def test_reconciliation_decision_link_repository_saves_and_retrieves_link():
    repository = ReconciliationDecisionLinkRepository()
    link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-1",
        decision_explanation_reference="DECISION-EXPLANATION-1",
        reconciliation_record_references=["RECONCILIATION-1"],
        source_document_reference="statement.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )

    repository.save(link)

    assert repository.get(link.reconciliation_decision_link_id) == link


def test_reconciliation_decision_link_repository_lists_all_links():
    repository = ReconciliationDecisionLinkRepository()
    first_link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-1",
        decision_explanation_reference="DECISION-EXPLANATION-1",
        reconciliation_record_references=["RECONCILIATION-1"],
        source_document_reference="statement.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )
    second_link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-2",
        decision_explanation_reference="DECISION-EXPLANATION-2",
        reconciliation_record_references=["RECONCILIATION-2"],
        source_document_reference="statement-2.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )

    repository.save(first_link)
    repository.save(second_link)

    assert repository.list_all() == [first_link, second_link]


def test_reconciliation_decision_link_repository_rejects_overwrite():
    repository = ReconciliationDecisionLinkRepository()
    link = ReconciliationDecisionLink.create(
        trust_record_reference="TRUST-1",
        decision_explanation_reference="DECISION-EXPLANATION-1",
        reconciliation_record_references=["RECONCILIATION-1"],
        source_document_reference="statement.pdf",
        rule_reference="RECONCILIATION_RECORD_REFERENCES_CAPTURED",
    )

    repository.save(link)

    with pytest.raises(ValueError, match="cannot be overwritten"):
        repository.save(link)


def test_reconciliation_decision_link_repository_returns_none_for_missing_link():
    repository = ReconciliationDecisionLinkRepository()

    assert repository.get("RECONCILIATION-DECISION-LINK-MISSING") is None