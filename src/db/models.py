from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    severity = Column(Integer, nullable=False)
    opened_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=False)
    resolution_time_min = Column(Float, nullable=False)
    sla_target_min = Column(Float, nullable=False)
    sla_breached = Column(Boolean, nullable=False)

    def __repr__(self):
        return (
            f"<Incident(id={self.id}, "
            f"incident_id='{self.incident_id}', "
            f"category='{self.category}', "
            f"severity={self.severity})>"
        )
