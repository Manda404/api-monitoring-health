"""
Définition des métriques Prometheus.

Pourquoi ?
- Les métriques doivent être définies "une fois" et réutilisées.
- Ici on choisit volontairement des métriques standards d'API monitoring:
  - Counter: trafic + erreurs
  - Histogram: latence (pour p95/p99)
  - Gauge: requêtes en cours (saturation)
  - Counter métier: distribution des bands
"""

from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

# 1) TRAFIC + ERREURS
API_REQUESTS_TOTAL = Counter(
    "api_requests_total",
    "Total number of HTTP requests",
    ["endpoint", "method", "http_status"]
)

# 2) LATENCE (histogram -> quantiles côté Prometheus)
API_REQUEST_LATENCY_SECONDS = Histogram(
    "api_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint", "method"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.8, 1.2, 2.0, 3.0)
)

# 3) SATURATION (simple proxy)
API_IN_PROGRESS = Gauge(
    "api_in_progress_requests",
    "In-progress HTTP requests",
    ["endpoint", "method"]
)

# 4) METIER
PREDICTIONS_TOTAL = Counter(
    "api_predictions_total",
    "Total predictions produced",
    ["risk_band"]
)

metrics_router = APIRouter()


@metrics_router.get("/metrics")
def metrics():
    """
    Endpoint scrappé par Prometheus.

    Pourquoi un endpoint dédié ?
    - Prometheus fonctionne en mode pull.
    - L'application expose son état via /metrics.
        
    IMPORTANT:
        - Prometheus attend du texte brut (text/plain)
        - PAS du JSON
        - On doit donc utiliser Response explicitement
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )