from sqlalchemy import text
from datetime import date
from src.core.database import engine


def get_operational_metrics(severity=None):
    query = """
        SELECT *
        FROM vw_operational_metrics
        WHERE 1=1
    """

    params = {}

    if severity:
        query += " AND severity = :severity"
        params["severity"] = severity

    query += " ORDER BY severity"

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = result.fetchall()

    return [dict(row._mapping) for row in rows]


def get_daily_metrics(start_date=None, end_date=None, severity=None):
    query = """
        SELECT *
        FROM vw_operational_metrics_daily
        WHERE 1=1
    """

    params = {}

    if start_date:
        query += " AND day >= :start_date"
        params["start_date"] = start_date

    if end_date:
        query += " AND day <= :end_date"
        params["end_date"] = end_date

    if severity:
        query += " AND severity = :severity"
        params["severity"] = severity

    query += " ORDER BY day, severity"

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = result.fetchall()

    return [dict(row._mapping) for row in rows]
