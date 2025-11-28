from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class CalorieTargetModel(Base):
    __tablename__ = "calorie_targets"

    _UTC_MINUS_5 = timezone(timedelta(hours=-5))
    patient_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    calories = Column(Float, nullable=False)
    protein_grams = Column(Float, nullable=False)
    carb_grams = Column(Float, nullable=False)
    fat_grams = Column(Float, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(CalorieTargetModel._UTC_MINUS_5),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(CalorieTargetModel._UTC_MINUS_5),
    )
