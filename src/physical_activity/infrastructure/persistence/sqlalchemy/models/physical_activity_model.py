from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, Float, String

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class PhysicalActivityModel(Base):
    __tablename__ = "physical_activities"

    id = Column(String(50), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(50), nullable=False, index=True)
    day = Column(Date, nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)
    duration_minutes = Column(Float, nullable=True)
    intensity = Column(String(20), nullable=True)
    calories_burned = Column(Float, nullable=False, default=0.0)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
