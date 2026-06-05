from trust_engine.application.trust_classifier import TrustClassifier


def test_trust_engine():
    from trust_engine.application.trust_score_calculator import TrustScoreCalculator
    
    score = TrustScoreCalculator().calculate(10, 0)
    classification = TrustClassifier().classify(score)
    
    
    assert score == 100.0
    assert classification.value == 'CLEAN_EXPORT'
    
