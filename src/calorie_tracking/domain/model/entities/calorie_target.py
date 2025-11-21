from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Tuple


@dataclass
class CalorieTarget:
    patient_id: str
    calories: float
    protein_grams: float
    carb_grams: float
    fat_grams: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        *,
        patient_id: str,
        calories: float,
        protein_grams: float,
        carb_grams: float,
        fat_grams: float,
    ) -> "CalorieTarget":
        now = datetime.now(timezone.utc)
        return cls(
            patient_id=patient_id,
            calories=calories,
            protein_grams=protein_grams,
            carb_grams=carb_grams,
            fat_grams=fat_grams,
            created_at=now,
            updated_at=now,
        )

    def apply_update(
        self,
        *,
        calories: float,
        protein_grams: float,
        carb_grams: float,
        fat_grams: float,
    ) -> None:
        self.calories = calories
        self.protein_grams = protein_grams
        self.carb_grams = carb_grams
        self.fat_grams = fat_grams
        self.updated_at = datetime.now(timezone.utc)
