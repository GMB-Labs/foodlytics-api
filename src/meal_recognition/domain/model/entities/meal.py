from dataclasses import dataclass
from typing import List, Optional


from src.shared.domain.model.entities.auditable_model import AuditableModel


class Meal(AuditableModel):
    id:str
    """
    Represents a meal with its nutritional information.
    """
    kcal: int
    #In grams
    carbs: float
    protein: float
    fat: float

