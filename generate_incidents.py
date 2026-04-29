import pandas as pd
import random
import uuid
import os
from datetime import datetime, timedelta

# -----------------------------
# Configurações Globais
# -----------------------------
NUM_RECORDS = 5000
SLA_TARGET = 40  # minutos
START_DATE = datetime.now() - timedelta(days=30)
END_DATE = datetime.now()

# -----------------------------
# Distribuições
# -----------------------------

categories = [
    ("Link Down", 0.25),
    ("Configuration Error", 0.20),
    ("Hardware Fault", 0.15),
    ("Partial Outage", 0.15),
    ("Power Failure", 0.10),
    ("Total Outage", 0.10),
    ("Weather Impact", 0.05)
]

severities = [
    (1, 0.50),
    (2, 0.35),
    (3, 0.15)
]

impact_scopes = [
    ("Regional", 0.60),
    ("Estadual", 0.30),
    ("Nacional", 0.10)
]

detected_by = [
    ("Monitoring", 0.50),
    ("Cliente", 0.35),
    ("NOC", 0.15)
]

ufs_brasil = [
    "SP","RJ","MG","ES","PR","SC","RS",
    "BA","PE","CE","GO","DF","MT","MS",
    "AM","PA","RO","RR","AP","TO",
    "MA","PI","RN","PB","AL","SE","AC"
]

# -----------------------------
# Função auxiliar ponderada
# -----------------------------
def weighted_choice(options):
    values = [opt[0] for opt in options]
    weights = [opt[1] for opt in options]
    return random.choices(values, weights=weights, k=1)[0]

# -----------------------------
# Geração dos registros
# -----------------------------
data = []

for _ in range(NUM_RECORDS):

    incident_id = str(uuid.uuid4())

    opened_at = START_DATE + timedelta(
        seconds=random.randint(0, int((END_DATE - START_DATE).total_seconds()))
    )

    severity = weighted_choice(severities)

    if severity == 1:
        resolution_time = random.randint(10, 45)
    elif severity == 2:
        resolution_time = random.randint(20, 80)
    else:
        resolution_time = random.randint(40, 180)

    closed_at = opened_at + timedelta(minutes=resolution_time)

    record = {
        "incident_id": incident_id,
        "opened_at": opened_at,
        "closed_at": closed_at,
        "category": weighted_choice(categories),
        "region": random.choice(ufs_brasil),
        "severity": severity,
        "impact_scope": weighted_choice(impact_scopes),
        "detected_by": weighted_choice(detected_by),
        "description": "Incident affecting network service",
        "resolution_time_min": resolution_time,
        "sla_target_min": SLA_TARGET,
        "sla_breached": resolution_time > SLA_TARGET
    }

    data.append(record)

# -----------------------------
# Criar DataFrame e salvar CSV
# -----------------------------
df = pd.DataFrame(data)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "sample_incidents.csv")

os.makedirs(os.path.join(BASE_DIR, "data", "raw"), exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Arquivo gerado com sucesso em: {OUTPUT_PATH}")