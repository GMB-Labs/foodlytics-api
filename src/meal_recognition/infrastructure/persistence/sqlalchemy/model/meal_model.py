from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, Float, String

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base

UTC_MINUS_5 = timezone(timedelta(hours=-5))

class MealModel(Base):
    __tablename__ = "meals"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    patient_id = Column(String, nullable=True)
    meal_type = Column(String, nullable=True)
    kcal = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fats = Column(Float, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC_MINUS_5))
