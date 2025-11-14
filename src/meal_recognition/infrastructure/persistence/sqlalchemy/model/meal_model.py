from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class MealModel(Base):
    __tablename__ = "meals"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    approximate_weight_in_grams = Column(Float, nullable=True)
    kcal = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fats = Column(Float, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
