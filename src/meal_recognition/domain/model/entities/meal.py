from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from src.meal_recognition.domain.model.valueobjects.meal_type import MealType


@dataclass
class Meal:
    id: str
    name: Optional[str]
    approximate_weight_in_grams: Optional[float]
    mealType: MealType
    kcal: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fats: Optional[float]
    uploaded_at: datetime

    @staticmethod
    def create(
        name: str,
        approx_w: float,
        meal_t: MealType,
        kcal: float,
        protein: float,
        carbs: float,
        fats: float
    ):
        return Meal(
            id=str(uuid4()),
            name=name,
            approximate_weight_in_grams=approx_w,
            mealType=meal_t,
            kcal=kcal,
            protein=protein,
            carbs=carbs,
            fats=fats,
            uploaded_at=datetime.utcnow()
        )
