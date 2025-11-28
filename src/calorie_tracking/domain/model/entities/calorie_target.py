from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
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
        utc_minus_5 = timezone(timedelta(hours=-5))
        now = datetime.now(utc_minus_5)
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
        utc_minus_5 = timezone(timedelta(hours=-5))
        self.updated_at = datetime.now(utc_minus_5)
