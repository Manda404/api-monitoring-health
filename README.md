# 🏥 Health API Monitoring Stack

Ce projet est une démonstration complète d'une architecture d'API moderne axée sur l'**observabilité**. Il simule une API de diagnostic de santé et met en œuvre une pile de monitoring complète pour suivre les performances techniques et les indicateurs métiers en temps réel.

---

## 🚀 Objectifs du Projet

L'enjeu n'est pas seulement de créer une API, mais de comprendre comment elle se comporte en production via les **Golden Signals** :

1. **Traffic** : Volume de requêtes (RPS/QPS).
2. **Errors** : Taux d'erreurs (4xx vs 5xx).
3. **Latency** : Temps de réponse (centré sur le p95/p99).
4. **Saturation** : Requêtes en cours et utilisation des ressources.
5. **Business Intelligence** : Distribution des niveaux de risque santé (Low, Medium, High, Critical).

---

## 🏗️ Architecture Technique

Le projet suit une structure modulaire pour garantir la séparation des responsabilités :

* **API (FastAPI)** : Service principal incluant une validation stricte via Pydantic et une instrumentation automatique via Middleware.
* **Simulator (Python)** : Générateur de trafic intelligent simulant des comportements réels (pics de charge, erreurs de données, pannes réseau).
* **Prometheus** : Base de données temporelle qui "scrappe" les métriques de l'API toutes les 5 secondes.
* **Grafana** : Interface de visualisation pré-configurée avec un dashboard professionnel.

---

## 📂 Structure du Code

```text
api-monitoring-health/
├── api/             # Code source de l'API FastAPI
├── simulator/       # Script de simulation de trafic
├── prometheus/      # Configuration du serveur de métriques
├── grafana/         # Provisioning des dashboards et datasources
└── docker-compose.yml

```

---

## 🛠️ Installation et Lancement

### Prérequis

* Docker & Docker Compose

### Démarrage rapide

```bash
# Cloner le projet
git clone <votre-url-repo>
cd api-monitoring-health

# Lancer la stack complète
docker compose up --build

```

---

## 📊 Points d'accès (Endpoints)

| Service | URL | Usage |
| --- | --- | --- |
| **API Docs** | `http://localhost:8000/docs` | Documentation Swagger/OpenAPI |
| **Prometheus** | `http://localhost:9090` | Requêtes directes (PromQL) |
| **Grafana** | `http://localhost:3000` | Dashboards (Login: `admin` / `admin`) |
| **Metrics** | `http://localhost:8000/metrics` | Données brutes pour Prometheus |

---

## 📉 Scénarios de Monitoring Observables

Le **Simulator** inclus génère différents types de signaux pour tester votre réactivité :

* **Cas Normaux** : Trafic régulier avec latence faible.
* **Cas Extrêmes** : Patients critiques provoquant une latence accrue (simulant un calcul complexe).
* **Cas Désastreux** : Envoi de données corrompues pour déclencher des erreurs 400 (Validation Error).
* **Bruit Réseau** : Timeouts volontaires pour tester la résilience.

---

## 📧 Contact

**Rostand Surel** - [rostandsurel@yahoo.com](mailto:rostandsurel@yahoo.com)

---

*Projet réalisé dans une démarche d'apprentissage du SRE (Site Reliability Engineering) et du développement d'APIs robustes.*

---
