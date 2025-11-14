from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
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
    uploaded_at = Column(DateTime, default=datetime.utcnow)
