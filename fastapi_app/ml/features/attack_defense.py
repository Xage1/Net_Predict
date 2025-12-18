"""
NetPredict ML Layer: attack_defense.py
Computes dynamic team attack & defense strengths weighted by recent matches.
"""

import numpy as np
import pandas as pd

def compute_attack_defense(df_matches, days_decay=30):
    """
    df_matches: DataFrame from DataLoader.load_matches()
    Returns DataFrame with home_attack, away_attack, home_defense, away_defense
    """

    df = df_matches.copy()
    df['home_attack'] = 0.0
    df['away_attack'] = 0.0
    df['home_defense'] = 0.0
    df['away_defense'] = 0.0

    # Simple weighted average over last N days
    for idx, row in df.iterrows():
        # Weight decay by date difference (in days)
        df_prev = df[df['date'] < row['date']]
        # Compute home attack
        home_past = df_prev[df_prev['home_team'] == row['home_team']]
        weights = np.exp(-(row['date'] - home_past['date']).dt.days / days_decay)
        if not home_past.empty:
            df.at[idx, 'home_attack'] = np.average(home_past['home_goals'], weights=weights)
            df.at[idx, 'home_defense'] = np.average(home_past['away_goals'], weights=weights)

        # Compute away attack
        away_past = df_prev[df_prev['away_team'] == row['away_team']]
        weights = np.exp(-(row['date'] - away_past['date']).dt.days / days_decay)
        if not away_past.empty:
            df.at[idx, 'away_attack'] = np.average(away_past['away_goals'], weights=weights)
            df.at[idx, 'away_defense'] = np.average(away_past['home_goals'], weights=weights)

    return df