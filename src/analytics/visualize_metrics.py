from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
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

DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# =============================
# LOAD DATA FROM VIEW
# =============================
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM vw_operational_metrics ORDER BY severity")
    )
    rows = result.fetchall()

severities = [row.severity for row in rows]
p95 = [row.p95_resolution for row in rows]
sla = [row.avg_sla_target for row in rows]
compliance = [float(row.sla_compliance) for row in rows]

# =============================
# GRÁFICO 1 — P95 vs SLA
# =============================
plt.figure()
plt.plot(severities, p95)
plt.plot(severities, sla)
plt.xlabel("Severity")
plt.ylabel("Minutes")
plt.title("P95 Resolution Time vs SLA Target")
plt.xticks(severities)
plt.savefig(os.path.join(DOCS_DIR, "p95_vs_sla.png"))
plt.close()

# =============================
# GRÁFICO 2 — SLA Compliance
# =============================
plt.figure()
plt.bar(severities, compliance)
plt.xlabel("Severity")
plt.ylabel("SLA Compliance (%)")
plt.title("SLA Compliance by Severity")
plt.xticks(severities)
plt.savefig(os.path.join(DOCS_DIR, "sla_compliance.png"))
plt.close()

print("Gráficos salvos em /docs")
