"""
NetPredict FastAPI Entry Point
Exposes ML-powered football prediction endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.predict import router as predict_router
from api.routes.health import router as health_router

app = FastAPI(
    title="NetPredict API",
    description="AI-powered football match prediction engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # lock down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])