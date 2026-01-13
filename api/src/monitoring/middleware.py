"""
Middleware d'instrumentation.

Pourquoi ?
- Sans middleware, on finit par instrumenter "à la main" chaque endpoint.
- Le middleware garantit une couverture globale (y compris 404/500).
- Il permet de calculer:
  - trafic total
  - latence globale
  - erreurs (4xx/5xx)
  - in-progress (saturation)
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.monitoring.metrics import (
    API_REQUESTS_TOTAL,
    API_REQUEST_LATENCY_SECONDS,
    API_IN_PROGRESS,
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        method = request.method

        start = time.time()
        API_IN_PROGRESS.labels(endpoint=endpoint, method=method).inc()

        try:
            response: Response = await call_next(request)
            status = str(response.status_code)
            return response
        except Exception:
            # Si exception non gérée -> 500
            status = "500"
            raise
        finally:
            duration = time.time() - start
            API_REQUEST_LATENCY_SECONDS.labels(endpoint=endpoint, method=method).observe(duration)
            API_REQUESTS_TOTAL.labels(endpoint=endpoint, method=method, http_status=status).inc()
            API_IN_PROGRESS.labels(endpoint=endpoint, method=method).dec()