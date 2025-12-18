"""
NetPredict Odds-Aware Calibration
Learns when to trust model vs market.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression

class OddsCalibrator:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, model_probs, market_probs, outcomes):
        X = np.column_stack([model_probs, market_probs])
        self.model.fit(X, outcomes)

    def calibrate(self, model_prob, market_prob):
        X = [[model_prob, market_prob]]
        return self.model.predict_proba(X)[0][1]
