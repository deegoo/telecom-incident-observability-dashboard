from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from datetime import date
from typing import List

from src.schemas.metrics_schema import DailyMetricsResponse
from src.services.metrics_service import (
    get_operational_metrics,
    get_daily_metrics
)

app = FastAPI(
    title="Telecom Incident NLP API",
    version="2.0.0"
)

app.router.redirect_slashes = False

# ==========================
# API
# ==========================
@app.get("/health")
def health():
    return {"status": "API running"}

@app.get("/metrics")
def metrics(severity: int | None = Query(None)):
    return get_operational_metrics(severity)

@app.get("/metrics/daily", response_model=List[DailyMetricsResponse])
def metrics_daily(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    severity: int | None = Query(None, ge=1, le=3)
):
    return get_daily_metrics(start_date, end_date, severity)

# ==========================
# FRONTEND (ÚLTIMO)
# ==========================
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)