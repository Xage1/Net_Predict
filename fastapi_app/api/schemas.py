"""
NetPredict API Schemas
Defines request & response contracts.
"""

from pydantic import BaseModel
from typing import Dict

class PredictionRequest(BaseModel):
    home_team: str
    away_team: str
    league: str
    match_date: str   # ISO date

class PredictionResponse(BaseModel):
    win_probabilities: Dict[str, float]
    score_probabilities: Dict[str, float]
