"""
Schémas d'entrée (contrat API).

Pourquoi ?
- Le monitoring dépend beaucoup d'un contrat stable.
- Une API "monitorable" commence par un schéma clair : sinon les 400 explosent.
- FastAPI s'appuie sur Pydantic pour valider automatiquement et documenter (/docs).
"""

from typing import Literal
from pydantic import BaseModel, Field


class PatientVitals(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Âge du patient")
    heart_rate: int = Field(..., ge=20, le=250, description="BPM")
    systolic_bp: int = Field(..., ge=60, le=260, description="Pression systolique")
    diastolic_bp: int = Field(..., ge=30, le=160, description="Pression diastolique")
    spo2: int = Field(..., ge=50, le=100, description="Saturation O2")
    temperature: float = Field(..., ge=30.0, le=45.0, description="Température (°C)")
    symptom: Literal[
        "none", "cough", "fever", "chest_pain", "shortness_of_breath"
    ] = "none"