"""
Centralise la configuration.

Pourquoi ?
- Éviter les "magic numbers" dispersés dans le code.
- Faciliter la modification des seuils et comportements sans toucher à la logique métier.
- Rendre explicite ce qui est "un choix produit" vs "un détail technique".
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Latence simulée (en secondes) : base + surcharge en fonction de la sévérité.
    base_latency_min_s: float = 0.02
    base_latency_max_s: float = 0.12
    extra_latency_per_severity_min_s: float = 0.05
    extra_latency_per_severity_max_s: float = 0.25

    # Taux d'erreur serveur simulé (5xx).
    simulated_5xx_rate: float = 0.03


settings = Settings()