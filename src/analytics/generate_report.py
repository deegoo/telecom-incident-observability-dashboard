import os
from sqlalchemy import create_engine, text
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

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

PDF_PATH = os.path.join(DOCS_DIR, "Operational_Report.pdf")

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# =============================
# FETCH DATA FROM VIEW
# =============================
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM vw_operational_metrics ORDER BY severity")
    )
    rows = result.fetchall()

# =============================
# BUILD PDF
# =============================
doc = SimpleDocTemplate(PDF_PATH, pagesize=A4)
elements = []
styles = getSampleStyleSheet()

# Title
elements.append(Paragraph("Telecom Incident Operational Report", styles["Heading1"]))
elements.append(Spacer(1, 0.3 * inch))

# Executive summary
elements.append(Paragraph(
    "This report presents operational performance metrics including "
    "average resolution time, P95 percentile, SLA target comparison, "
    "and SLA compliance by severity level.",
    styles["Normal"]
))
elements.append(Spacer(1, 0.4 * inch))

# Table
table_data = [["Severity", "Total", "Avg Resolution", "P95", "SLA Target", "Compliance (%)"]]

for row in rows:
    table_data.append([
        row.severity,
        row.total_incidents,
        round(row.avg_resolution, 2),
        round(row.p95_resolution, 2),
        round(row.avg_sla_target, 2),
        round(float(row.sla_compliance), 2)
    ])

table = Table(table_data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
]))

elements.append(table)
elements.append(Spacer(1, 0.5 * inch))

# Add images
elements.append(Paragraph("P95 vs SLA", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))
elements.append(
    Image(os.path.join(DOCS_DIR, "p95_vs_sla.png"), width=5*inch, height=3*inch)
)
elements.append(Spacer(1, 0.5 * inch))

elements.append(Paragraph("SLA Compliance by Severity", styles["Heading2"]))
elements.append(Spacer(1, 0.2 * inch))
elements.append(
    Image(os.path.join(DOCS_DIR, "sla_compliance.png"), width=5*inch, height=3*inch)
)

doc.build(elements)

print(f"PDF gerado com sucesso em: {PDF_PATH}")
