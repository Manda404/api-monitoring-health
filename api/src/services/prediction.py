"""
Logique métier de scoring.

Pourquoi ?
- Séparer "métier" de "transport HTTP" et de "monitoring".
- Le monitoring doit pouvoir évoluer sans toucher au scoring, et inversement.
"""

from src.schemas.input import PatientVitals


def compute_severity(v: PatientVitals) -> int:
    """
    Estime une "sévérité" utilisée pour simuler la latence.
    Plus c'est sévère, plus on simule du travail (et donc de la latence).
    """
    severity = 0
    if v.spo2 < 92:
        severity += 2
    if v.heart_rate > 120:
        severity += 1
    if v.temperature > 39.0:
        severity += 1
    if v.symptom in ("chest_pain", "shortness_of_breath"):
        severity += 2
    return severity


def predict_risk(v: PatientVitals) -> tuple[int, str]:
    """
    Retourne (risk_score, risk_band).

    Ici c'est volontairement simple :
    - L'objectif du projet n'est pas le ML,
      mais l'observabilité (latence, erreurs, trafic, métriques métier).
    """
    score = 0
    score += 2 if v.spo2 < 92 else 0
    score += 1 if v.spo2 < 88 else 0
    score += 1 if v.temperature > 38.5 else 0
    score += 1 if v.heart_rate > 110 else 0
    score += 1 if v.systolic_bp > 160 else 0
    score += 2 if v.symptom in ("chest_pain", "shortness_of_breath") else 0

    if score <= 1:
        band = "low"
    elif score <= 3:
        band = "medium"
    elif score <= 5:
        band = "high"
    else:
        band = "critical"

    return score, band