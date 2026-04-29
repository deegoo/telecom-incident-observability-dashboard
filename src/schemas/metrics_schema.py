from pydantic import BaseModel
from datetime import date


class DailyMetricsResponse(BaseModel):
    day: date
    severity: int
    total_incidents: int
    avg_resolution: float
    sla_compliance: float

    class Config:
        orm_mode = True