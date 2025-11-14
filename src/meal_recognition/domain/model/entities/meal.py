from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

@dataclass
class Meal:
    id: str
    name: Optional[str]
    approximate_weight_in_grams: Optional[float]
    kcal: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fats: Optional[float]
    uploaded_at: datetime

    @staticmethod
    def create(name, approx_w, kcal, protein, carbs, fats):
        return Meal(
            id=str(uuid4()),
            name=name,
            approximate_weight_in_grams=approx_w,
            kcal=kcal,
            protein=protein,
            carbs=carbs,
            fats=fats,
            uploaded_at=datetime.utcnow(),
        )
