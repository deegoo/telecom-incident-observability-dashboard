import pandas as pd
from sqlalchemy import text
from src.core.database import engine

CSV_PATH = "data/raw/sample_incidents.csv"


def load_data():

    df = pd.read_csv(CSV_PATH)

    df["opened_at"] = pd.to_datetime(df["opened_at"])

    records = [
        {
            "incident_date": row["opened_at"].date(),
            "severity": int(row["severity"]),
            "resolution": int(row["resolution_time_min"]),
            "sla": int(row["sla_target_min"])
        }
        for _, row in df.iterrows()
    ]

    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO incidents (
                incident_date,
                severity,
                resolution_time_minutes,
                sla_target_minutes
            )
            VALUES (
                :incident_date,
                :severity,
                :resolution,
                :sla
            )
            """),
            records
        )

    print(f"{len(df)} incidentes carregados.")


if __name__ == "__main__":
    load_data()