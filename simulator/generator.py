"""
Simulateur de trafic.

Pourquoi ?
- En monitoring, tu dois "créer des signaux" observables:
  - trafic variable (bursts)
  - erreurs de données (payload invalid -> 400)
  - timeouts réseau (bruit)
  - cas extrêmes (latence + risk_band)
"""

import random
import time
import requests

API_URL = "http://api:8000/predict"

P_EXTREME = 0.12
P_DISASTER = 0.06
P_BURST = 0.10
P_NETWORK_TIMEOUT = 0.04


def normal_payload():
    return {
        "age": random.randint(18, 90),
        "heart_rate": random.randint(55, 95),
        "systolic_bp": random.randint(105, 135),
        "diastolic_bp": random.randint(65, 85),
        "spo2": random.randint(95, 100),
        "temperature": round(random.uniform(36.2, 37.5), 1),
        "symptom": random.choice(["none", "cough", "fever"]),
    }


def extreme_payload():
    return {
        "age": random.randint(40, 95),
        "heart_rate": random.randint(120, 170),
        "systolic_bp": random.randint(160, 220),
        "diastolic_bp": random.randint(95, 130),
        "spo2": random.randint(82, 92),
        "temperature": round(random.uniform(38.5, 41.0), 1),
        "symptom": random.choice(["fever", "chest_pain", "shortness_of_breath"]),
    }


def disaster_payload():
    payload = normal_payload()
    mode = random.choice(["missing_field", "wrong_type", "absurd_value"])

    if mode == "missing_field":
        payload.pop(random.choice(list(payload.keys())))
    elif mode == "wrong_type":
        payload[random.choice(list(payload.keys()))] = "oops"
    else:
        payload["heart_rate"] = random.choice([-10, 9999])
    return payload


def choose_payload():
    r = random.random()
    if r < P_DISASTER:
        return disaster_payload()
    if r < P_DISASTER + P_EXTREME:
        return extreme_payload()
    return normal_payload()


def next_sleep_seconds():
    # Arrivées ~ exponentielles (classique pour simuler du trafic)
    base_rate = 1.2
    if random.random() < P_BURST:
        base_rate = 6.0
    return random.expovariate(base_rate)


def main():
    while True:
        payload = choose_payload()
        timeout = random.uniform(0.05, 1.5)

        try:
            if random.random() < P_NETWORK_TIMEOUT:
                timeout = 0.01  # timeout volontaire
            requests.post(API_URL, json=payload, timeout=timeout)
        except requests.exceptions.RequestException:
            pass

        time.sleep(next_sleep_seconds())


if __name__ == "__main__":
    main()