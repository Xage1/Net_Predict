"""
NetPredict ML Layer: poisson_glm.py
Trains Poisson regression models for home & away goals.
"""

import statsmodels.api as sm
import pandas as pd

class PoissonModel:
    def __init__(self):
        self.model_home = None
        self.model_away = None

    def train(self, df_features):
        """
        df_features must include columns:
        home_attack, away_defense, away_attack, home_defense, league_tier, home_advantage
        """
        X_home = df_features[['home_attack', 'away_defense', 'league_tier']]
        y_home = df_features['home_goals']
        X_home = sm.add_constant(X_home)
        self.model_home = sm.GLM(y_home, X_home, family=sm.families.Poisson()).fit()

        X_away = df_features[['away_attack', 'home_defense', 'league_tier']]
        y_away = df_features['away_goals']
        X_away = sm.add_constant(X_away)
        self.model_away = sm.GLM(y_away, X_away, family=sm.families.Poisson()).fit()

    def predict_lambda(self, df_features):
        """
        Returns DataFrame with dynamic λ_home and λ_away for simulations
        """
        X_home = df_features[['home_attack', 'away_defense', 'league_tier']]
        X_home = sm.add_constant(X_home)
        df_features['lambda_home'] = self.model_home.predict(X_home)

        X_away = df_features[['away_attack', 'home_defense', 'league_tier']]
        X_away = sm.add_constant(X_away)
        df_features['lambda_away'] = self.model_away.predict(X_away)

        return df_features