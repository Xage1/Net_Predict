"""
NetPredict Prediction Endpoint
Runs full ML pipeline: features → Poisson → Monte Carlo.
"""

from fastapi import APIRouter, HTTPException
from api.schemas import PredictionRequest, PredictionResponse

from ml.data_loader import DataLoader
from ml.features.attack_defense import compute_attack_defense
from ml.models.poisson_glm import PoissonModel
from ml.simulation.monte_carlo import simulate_match

router = APIRouter()

# NOTE:
# In production, load trained models from model_store
poisson_model = PoissonModel()

@router.post("/", response_model=PredictionResponse)
def predict_match(payload: PredictionRequest):
    """
    Predicts football match outcome using NetPredict AI.
    """

    # 1️⃣ Load historical data for training context
    df_matches = DataLoader.load_matches(leagues=[payload.league])

    if df_matches.empty:
        raise HTTPException(status_code=404, detail="No match data available")

    # 2️⃣ Feature engineering
    df_features = compute_attack_defense(df_matches)

    # 3️⃣ Train Poisson model (offline later)
    poisson_model.train(df_features)

    # 4️⃣ Extract latest match-like row
    latest = df_features.iloc[-1:].copy()

    # 5️⃣ Predict base λ values
    latest = poisson_model.predict_lambda(latest)

    lambda_home = float(latest["lambda_home"].iloc[0])
    lambda_away = float(latest["lambda_away"].iloc[0])

    # 6️⃣ Monte Carlo simulation
    score_dist, win_probs = simulate_match(
        lambda_home=lambda_home,
        lambda_away=lambda_away,
        sims=10000
    )

    # Normalize score distribution
    total = sum(score_dist.values())
    score_probs = {
        f"{k[0]}-{k[1]}": round(v / total, 4)
        for k, v in score_dist.items()
    }

    return PredictionResponse(
        win_probabilities={
            "home_win": round(win_probs["home_win"], 4),
            "draw": round(win_probs["draw"], 4),
            "away_win": round(win_probs["away_win"], 4),
        },
        score_probabilities=score_probs
    )