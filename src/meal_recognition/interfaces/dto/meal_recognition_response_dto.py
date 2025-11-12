from pydantic import BaseModel
from typing import Optional

class MealRecognitionResponseDTO(BaseModel):
    name: Optional[str] = None
    approximate_weight_in_grams: Optional[str] = None
    kcal: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
