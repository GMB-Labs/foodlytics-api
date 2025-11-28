from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime, timedelta, timezone
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base

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
    _UTC_MINUS_5 = timezone(timedelta(hours=-5))
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(MealModel._UTC_MINUS_5))
