from sqlalchemy import create_engine, text

# CONFIG
USER = "postgres"
PASSWORD = "1406"
HOST = "localhost"
PORT = "5432"
DATABASE = "telecom_incidents"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

with engine.connect() as conn:

    print("\n===== MÉTRICAS OPERACIONAIS (POSTGRESQL) =====")

    # MTTR Geral
    mttr = conn.execute(
        text("SELECT AVG(resolution_time_min) FROM incidents")
    ).scalar()

    print(f"MTTR Geral: {mttr:.2f} minutos")

    # SLA Compliance
    sla = conn.execute(
        text("""
            SELECT 
                100.0 * SUM(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END) 
                / COUNT(*) 
            FROM incidents
        """)
    ).scalar()

    print(f"SLA Compliance: {sla:.2f}%")

    # MTTR por Categoria
    print("\nMTTR por Categoria:")

    result = conn.execute(
        text("""
            SELECT category, AVG(resolution_time_min) as avg_mttr
            FROM incidents
            GROUP BY category
            ORDER BY avg_mttr DESC
        """)
    )

    for row in result:
        print(f"{row.category}: {row.avg_mttr:.2f} min")

    # SLA por Severidade
    print("\nSLA Compliance por Severidade:")

    result = conn.execute(
        text("""
            SELECT 
                severity,
                100.0 * SUM(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END) 
                / COUNT(*) as sla_rate
            FROM incidents
            GROUP BY severity
            ORDER BY severity
        """)
    )

    for row in result:
        print(f"Severidade {row.severity}: {row.sla_rate:.2f}%")
