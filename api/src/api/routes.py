"""
Routes HTTP (contrat).

Pourquoi ?
- Les routes doivent rester courtes: recevoir -> appeler service -> répondre.
- Le monitoring est assuré par middleware + compteurs métier.
"""

import random
import time
from fastapi import APIRouter, HTTPException

from src.schemas.input import PatientVitals
from src.schemas.output import PredictionResponse
from src.services.prediction import compute_severity, predict_risk
from src.config.settings import settings
from src.monitoring.metrics import PREDICTIONS_TOTAL

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict(v: PatientVitals):
    # 1) Simuler de la charge/latence (pédagogique pour p95/p99)
    severity = compute_severity(v)

    base = random.uniform(settings.base_latency_min_s, settings.base_latency_max_s)
    extra = severity * random.uniform(
        settings.extra_latency_per_severity_min_s,
        settings.extra_latency_per_severity_max_s
    )
    time.sleep(base + extra)

    # 2) Simuler une panne serveur rare (pédagogique pour error-rate 5xx)
    if random.random() < settings.simulated_5xx_rate:
        raise HTTPException(status_code=500, detail="Simulated internal error")

    # 3) Prédiction métier
    score, band = predict_risk(v)

    # 4) Métrique métier
    PREDICTIONS_TOTAL.labels(risk_band=band).inc()

    return PredictionResponse(risk_score=score, risk_band=band)