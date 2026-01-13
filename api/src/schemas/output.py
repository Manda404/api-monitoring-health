"""
Schémas de sortie.

Pourquoi ?
- Un contrat de sortie explicite permet :
  - tests simples
  - dashboards métier (ex: distribution des bands)
  - comparaison entre versions d'API
"""

from typing import Literal
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    risk_score: int
    risk_band: Literal["low", "medium", "high", "critical"]