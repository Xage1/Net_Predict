"""
NetPredict Health Check Endpoint
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "NetPredict",
        "model": "Dynamic Poisson + Monte Carlo"
    }