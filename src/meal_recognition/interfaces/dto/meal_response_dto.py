from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.meal_recognition.domain.model.valueobjects.meal_type import MealType


class MealResponseDTO(BaseModel):
    id: str
    name: Optional[str] = None
    patient_id: str
    meal_t: Optional[MealType] = None
    kcal: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    uploaded_at: datetime
