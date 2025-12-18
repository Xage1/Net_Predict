"""
NetPredict ML Layer: monte_carlo.py
Simulates matches minute-by-minute using dynamic Poisson λ(t).
"""

import numpy as np
import pandas as pd

def simulate_match(lambda_home, lambda_away, minutes=90, sims=10000, seed=42):
    """
    Returns:
    - DataFrame: distribution of scores
    - win/draw/loss probabilities
    """
    np.random.seed(seed)
    results = []

    # Convert total λ into per-minute rates
    lambda_home_min = lambda_home / minutes
    lambda_away_min = lambda_away / minutes

    for _ in range(sims):
        home_goals = np.random.poisson(lambda_home_min, minutes).sum()
        away_goals = np.random.poisson(lambda_away_min, minutes).sum()
        results.append((home_goals, away_goals))

    df = pd.DataFrame(results, columns=['home_goals', 'away_goals'])
    probs = {
        'home_win': np.mean(df['home_goals'] > df['away_goals']),
        'draw': np.mean(df['home_goals'] == df['away_goals']),
        'away_win': np.mean(df['home_goals'] < df['away_goals'])
    }
    score_dist = df.value_counts().sort_index().to_dict()
    return score_dist, probs