from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, Float, String, PrimaryKeyConstraint, UniqueConstraint

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class DailyIntakeSummaryModel(Base):
    __tablename__ = "daily_intake_summaries"
    id = Column(String(50), primary_key=True, default=lambda: str(uuid4()))
    patient_id = Column(String(50), nullable=False)
    day = Column(Date, nullable=False)

    target_calories = Column(Float, nullable=False)
    target_protein = Column(Float, nullable=False)
    target_carbs = Column(Float, nullable=False)
    target_fats = Column(Float, nullable=False)

    consumed_calories = Column(Float, nullable=False)
    consumed_protein = Column(Float, nullable=False)
    consumed_carbs = Column(Float, nullable=False)
    consumed_fats = Column(Float, nullable=False)
    activity_burned = Column(Float, nullable=False, default=0.0)
    activity_type = Column(String(50), nullable=True)
    activity_duration_minutes = Column(Float, nullable=True)

    status = Column(String(30), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint("patient_id", "day", name="uq_daily_intake_summary_patient_day"),
    )
