from pydantic import BaseModel
from typing import Optional

class MealRecognitionResponseDTO(BaseModel):
    name: str
    approximate_weight: float
    kcal: float
    protein: float
    carbs: float
    fats: float
