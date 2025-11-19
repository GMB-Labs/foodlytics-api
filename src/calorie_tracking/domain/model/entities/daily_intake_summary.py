from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone


@dataclass
class DailyIntakeSummary:
    day: date
    patient_id: str
    target_calories: float
    target_protein: float
    target_carbs: float
    target_fats: float
    consumed_calories: float
    consumed_protein: float
    consumed_carbs: float
    consumed_fats: float
    activity_burned: float
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        *,
        day: date,
        patient_id: str,
        target_calories: float,
        target_protein: float,
        target_carbs: float,
        target_fats: float,
        consumed_calories: float,
        consumed_protein: float,
        consumed_carbs: float,
        consumed_fats: float,
        activity_burned: float,
        status: str,
    ) -> "DailyIntakeSummary":
        now = datetime.now(timezone.utc)
        return cls(
            day=day,
            patient_id=patient_id,
            target_calories=target_calories,
            target_protein=target_protein,
            target_carbs=target_carbs,
            target_fats=target_fats,
            consumed_calories=consumed_calories,
            consumed_protein=consumed_protein,
            consumed_carbs=consumed_carbs,
            consumed_fats=consumed_fats,
            activity_burned=activity_burned,
            status=status,
            created_at=now,
            updated_at=now,
        )

    def apply_update(
        self,
        *,
        target_calories: float,
        target_protein: float,
        target_carbs: float,
        target_fats: float,
        consumed_calories: float,
        consumed_protein: float,
        consumed_carbs: float,
        consumed_fats: float,
        activity_burned: float,
        status: str,
    ) -> None:
        self.target_calories = target_calories
        self.target_protein = target_protein
        self.target_carbs = target_carbs
        self.target_fats = target_fats
        self.consumed_calories = consumed_calories
        self.consumed_protein = consumed_protein
        self.consumed_carbs = consumed_carbs
        self.consumed_fats = consumed_fats
        self.activity_burned = activity_burned
        self.status = status
        self.updated_at = datetime.now(timezone.utc)
