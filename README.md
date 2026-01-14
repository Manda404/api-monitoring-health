# Health Risk API - Monitoring & Observability

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)](https://grafana.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)

> Un projet d'apprentissage professionnel démontrant les bonnes pratiques de monitoring d'API avec Prometheus et Grafana.

**Auteur :** Rostand Surel  
**Contact :** rostandsurel@yahoo.com

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Architecture](#-architecture)
- [Métriques surveillées](#-métriques-surveillées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Technologies](#-technologies)
- [Apprentissages clés](#-apprentissages-clés)
- [Roadmap](#-roadmap)

---

## 🎯 Présentation

Ce projet implémente une **API de prédiction de risque santé** entièrement instrumentée pour le monitoring. L'objectif principal est pédagogique : comprendre et maîtriser les **Golden Signals** et les métriques essentielles pour surveiller une API en production.

### Cas d'usage

L'API évalue le risque médical d'un patient à partir de ses signes vitaux (fréquence cardiaque, saturation en oxygène, température, etc.) et retourne un score de risque classé en quatre catégories : `low`, `medium`, `high`, `critical`.

### Pourquoi ce projet ?

- **Apprendre le monitoring d'API** sans se perdre dans la complexité du métier
- Comprendre les **Golden Signals** (Traffic, Errors, Latency, Saturation)
- Maîtriser **Prometheus + Grafana** en contexte réaliste
- Observer l'impact des anomalies (bursts, erreurs, latence) sur les métriques
- Adopter une **architecture propre et professionnelle** (séparation des couches, documentation)

---

## 🏗️ Architecture

Le projet utilise une architecture microservices orchestrée avec **Docker Compose** :

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Simulator   │─────▶│   FastAPI    │◀────▶│  Prometheus  │
│  (Traffic)   │      │     API      │      │   (Scraper)  │
└──────────────┘      └──────────────┘      └──────┬───────┘
                             │                     │
                             │                     │
                             ▼                     ▼
                      ┌──────────────┐      ┌──────────────┐
                      │   /metrics   │      │   Grafana    │
                      │  (Endpoint)  │      │ (Dashboard)  │
                      └──────────────┘      └──────────────┘
```

### Composants

| Composant | Rôle | Port |
|-----------|------|------|
| **API** | FastAPI exposant `/predict` et `/metrics` | 8000 |
| **Simulator** | Générateur de trafic (normal, extrême, invalide) | - |
| **Prometheus** | Collecte et stockage des métriques | 9090 |
| **Grafana** | Visualisation et dashboards | 3000 |

---

## 📊 Métriques surveillées

### 1. Golden Signals

#### **Traffic** (Trafic)
- `api_requests_total` : Nombre total de requêtes
- Agrégation : RPS (Requests Per Second)

#### **Errors** (Erreurs)
- **4xx** : Erreurs client (payload invalide, validation)
- **5xx** : Erreurs serveur (pannes simulées)
- Taux d'erreur calculé sur 5 minutes

#### **Latency** (Latence)
- `api_request_latency_seconds` : Distribution des temps de réponse
- Quantiles : **p50, p95, p99**
- Buckets : de 10ms à 3s

#### **Saturation**
- `api_in_progress_requests` : Requêtes en cours de traitement
- Indicateur de charge instantanée

### 2. Métriques métier

- `api_predictions_total{risk_band}` : Distribution des prédictions par niveau de risque
- Permet d'observer l'impact métier (taux de cas critiques/minute)

### 3. Qualité des données (à venir)

- `api_payload_validation_errors_total` : Comptage des erreurs de validation Pydantic

---

## ✅ Prérequis

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- 4 GB RAM disponibles
- Ports **3000**, **8000**, **9090** libres

---

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone <votre-repo>
cd api-monitoring-health
```

### 2. Lancer l'infrastructure

```bash
docker compose up --build
```

Lors du premier lancement, Docker va :
- Construire les images (`api`, `simulator`)
- Télécharger Prometheus et Grafana
- Démarrer les 4 services

### 3. Vérifier le démarrage

```bash
# API en ligne
curl http://localhost:8000/health
# → {"status":"ok"}

# Métriques exposées
curl http://localhost:8000/metrics
# → Métriques Prometheus (format texte)
```

---

## 💻 Utilisation

### Accès aux interfaces

| Service | URL | Identifiants |
|---------|-----|--------------|
| **API Documentation** | http://localhost:8000/docs | - |
| **Métriques brutes** | http://localhost:8000/metrics | - |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | `admin` / `admin` |

### Tester l'API manuellement

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "heart_rate": 145,
    "systolic_bp": 170,
    "diastolic_bp": 100,
    "spo2": 88,
    "temperature": 39.2,
    "symptom": "chest_pain"
  }'
```

Réponse attendue :
```json
{
  "risk_score": 8,
  "risk_band": "critical"
}
```

### Observer dans Grafana

1. Ouvrir http://localhost:3000
2. Se connecter (`admin` / `admin`)
3. Naviguer vers **Dashboards → API Monitoring → Health API - Monitoring Core**

Vous verrez :
- **RPS** : Pics lors des bursts (probabilité 10%)
- **4xx** : Augmentation lors des payloads invalides (6%)
- **5xx** : Erreurs serveur simulées (3%)
- **p95 Latency** : Impact des cas extrêmes (charge CPU simulée)
- **Risk bands** : Distribution métier des prédictions

---

## 📁 Structure du projet

```
api-monitoring-health/
├── docker-compose.yml           # Orchestration des services
├── README.md
│
├── api/                         # Service API
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py             # Point d'entrée FastAPI
│       ├── api/
│       │   └── routes.py       # Endpoints HTTP
│       ├── schemas/
│       │   ├── input.py        # Contrat d'entrée (Pydantic)
│       │   └── output.py       # Contrat de sortie
│       ├── services/
│       │   └── prediction.py   # Logique métier (scoring)
│       ├── monitoring/
│       │   ├── metrics.py      # Définition des métriques Prometheus
│       │   └── middleware.py   # Instrumentation automatique
│       └── config/
│           └── settings.py     # Configuration centralisée
│
├── simulator/                   # Générateur de trafic
│   ├── Dockerfile
│   ├── requirements.txt
│   └── generator.py            # Scénarios (normal/extrême/disaster)
│
├── prometheus/
│   └── prometheus.yml          # Configuration de scraping
│
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── datasource.yml  # Connexion Prometheus
        └── dashboards/
            ├── dashboard.yml
            └── health-api-dashboard.json
```

---

## 🛠️ Technologies

| Catégorie | Stack |
|-----------|-------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Monitoring** | Prometheus, prometheus-client |
| **Visualisation** | Grafana |
| **Conteneurisation** | Docker, Docker Compose |
| **Langage** | Python 3.11 |

---

## 💡 Apprentissages clés

### 1. Architecture en couches

- **Séparation claire** : routes, services, schemas, monitoring
- **Testabilité** : chaque module est isolé et testable
- **Maintenabilité** : ajout de fonctionnalités sans toucher au core

### 2. Instrumentation professionnelle

- **Middleware** : couverture automatique de tous les endpoints
- **Métriques centralisées** : définies une fois, réutilisées partout
- **Pas de "magic numbers"** : configuration explicite (`settings.py`)

### 3. Observabilité

- **Golden Signals** : les 4 piliers du monitoring d'API
- **Quantiles** : p95/p99 révèlent les latences extrêmes (moyenne = illusion)
- **Labels** : segmentation par endpoint, method, status, risk_band

### 4. Simulation réaliste

- **Trafic variable** : bursts, arrivées exponentielles
- **Erreurs contrôlées** : 4xx (validation), 5xx (pannes)
- **Latence corrélée** : les cas critiques coûtent plus cher en temps

---

## 🗺️ Roadmap

### Phase 1 : Monitoring core ✅
- [x] API FastAPI instrumentée
- [x] Golden Signals (Traffic, Errors, Latency, Saturation)
- [x] Dashboard Grafana
- [x] Simulateur de trafic

### Phase 2 : Qualité des données
- [ ] Métrique `api_payload_validation_errors_total`
- [ ] Dashboard dédié à la validation (champs manquants, types incorrects)
- [ ] Alertes Prometheus (taux d'erreur > seuil)

### Phase 3 : Dashboard métier
- [ ] Dashboard Streamlit ou Grafana orienté "produit"
- [ ] Tendances risk_band (évolution sur 24h)
- [ ] Détection d'anomalies métier

### Phase 4 : Production-ready
- [ ] Logging structuré (JSON)
- [ ] Tracing distribué (OpenTelemetry)
- [ ] Tests de charge (Locust)
- [ ] CI/CD (GitHub Actions)

---

## 📧 Contact

**Rostand Surel**  
Email : [rostandsurel@yahoo.com](mailto:rostandsurel@yahoo.com)

---

## 📄 Licence

Ce projet est à but pédagogique. Vous êtes libre de l'utiliser, le modifier et le partager.

---

**Bonne exploration du monitoring ! 🚀📊**