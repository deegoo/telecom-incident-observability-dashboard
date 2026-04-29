import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Incident
import os

# =============================
# CONFIG
# =============================
USER = "postgres"
PASSWORD = "1406"
HOST = "localhost"
PORT = "5432"
DATABASE = "telecom_incidents"

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "sample_incidents.csv")


# =============================
# ENGINE & SESSION
# =============================
engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

Session = sessionmaker(bind=engine)
session = Session()


# =============================
# LOAD CSV
# =============================
df = pd.read_csv(CSV_PATH)

# Converter datas
df["opened_at"] = pd.to_datetime(df["opened_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

# =============================
# INSERT DATA
# =============================
for _, row in df.iterrows():
    incident = Incident(
        incident_id=row["incident_id"],
        category=row["category"],
        severity=row["severity"],
        opened_at=row["opened_at"],
        closed_at=row["closed_at"],
        resolution_time_min=row["resolution_time_min"],
        sla_target_min = row["sla_target_min"],
        sla_breached=row["sla_breached"],
    )
    session.add(incident)

session.commit()
session.close()

print(f"{len(df)} registros inseridos com sucesso.")
