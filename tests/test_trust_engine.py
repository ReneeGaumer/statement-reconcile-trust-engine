from trust_engine.application.trust_score_calculator import TrustScoreCalculator
from trust_engine.application.trust_classifier import TrustClassifier

score = TrustScoreCalculator().calculate(10, 0)
classification = TrustClassifier().classify(score)

print('Trust Score:', score)
print('Classification:', classification.value)

assert score == 100.0
assert classification.value == 'CLEAN_EXPORT'

print('PASS')
