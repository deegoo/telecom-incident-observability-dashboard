from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "API running"}

@app.get("/metrics")
def metrics(severity: int | None = Query(None)):
    return get_operational_metrics(severity)

@app.get(
    "/metrics/daily",
    response_model=List[DailyMetricsResponse],
    summary="Daily operational metrics with optional filters",
    tags=["Analytics"]
)
def metrics_daily(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    severity: int | None = Query(None, ge=1, le=3)
):
    return get_daily_metrics(start_date, end_date, severity)

