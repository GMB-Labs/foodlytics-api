from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from src.meal_recognition.domain.model.valueobjects.meal_type import MealType


@dataclass
class Meal:
    id: str
    name: Optional[str]
    patient_id: str
    mealType: MealType
    kcal: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fats: Optional[float]
    uploaded_at: datetime

    @staticmethod
    def create(
        name: str,
        patient_id: str,
        meal_t: MealType,
        kcal: float,
        protein: float,
        carbs: float,
        fats: float
    ):
        peru_tz = timezone(timedelta(hours=-5))
        return Meal(
            id=str(uuid4()),
            name=name,
            patient_id=patient_id,
            mealType=meal_t,
            kcal=kcal,
            protein=protein,
            carbs=carbs,
            fats=fats,
            uploaded_at=datetime.now(peru_tz)
        )
