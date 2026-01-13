"""
Point d'entrée FastAPI.

Pourquoi ?
- Ici on assemble seulement:
  - routes
  - middleware
  - metrics endpoint
- C'est volontairement "léger" : la lisibilité vient de la séparation des couches.
"""

from fastapi import FastAPI

from src.api.routes import router
from src.monitoring.metrics import metrics_router
from src.monitoring.middleware import PrometheusMiddleware

app = FastAPI(title="Health Risk API (Monitoring-ready)")

# Instrumentation globale
app.add_middleware(PrometheusMiddleware)

# Endpoints
app.include_router(router)
app.include_router(metrics_router)