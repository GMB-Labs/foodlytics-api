from pydantic import BaseModel
from typing import List, Optional


class MealItemDTO(BaseModel):
    name: str
    approximate_weight: float
    kcal_per_gram: float
    protein_per_gram: float
    carbs_per_gram: float
    fats_per_gram: float


class MealRecognitionResponseDTO(BaseModel):
    items: List[MealItemDTO]
