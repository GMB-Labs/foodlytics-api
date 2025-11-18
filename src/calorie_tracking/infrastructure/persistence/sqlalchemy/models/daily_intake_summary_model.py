from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Float, String, PrimaryKeyConstraint

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class DailyIntakeSummaryModel(Base):
    __tablename__ = "daily_intake_summaries"
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
        PrimaryKeyConstraint("patient_id", "day", name="pk_daily_intake_summary"),
    )
