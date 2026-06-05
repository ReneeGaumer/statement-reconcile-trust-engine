from trust_engine.application.trust_classifier import TrustClassifier
from trust_engine.exceptions.trust_classification import TrustClassification


def test_trust_classifier():
    classifier = TrustClassifier()

    assert (
        classifier.classify(100, False)
        == TrustClassification.CLEAN_EXPORT
    )

    assert (
        classifier.classify(80, False)
        == TrustClassification.EXPORT_WITH_WARNINGS
    )

    assert (
        classifier.classify(60, False)
        == TrustClassification.PARTIAL_EXPORT
    )

    assert (
        classifier.classify(40, False)
        == TrustClassification.UNSAFE_EXPORT
    )

    assert (
        classifier.classify(100, True)
        == TrustClassification.EXPORT_EMBARGO
    )