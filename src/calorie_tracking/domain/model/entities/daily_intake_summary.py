from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from src.calorie_tracking.domain.model.value_objects.daily_summary_status import DailySummaryStatus


@dataclass
class DailyIntakeSummary:
    id: str
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
    activity_type: Optional[str]
    activity_duration_minutes: Optional[float]
    status: DailySummaryStatus
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
        activity_type: Optional[str],
        activity_duration_minutes: Optional[float],
        status: DailySummaryStatus,
    ) -> "DailyIntakeSummary":
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
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
            activity_type=activity_type,
            activity_duration_minutes=activity_duration_minutes,
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
        activity_type: Optional[str],
        activity_duration_minutes: Optional[float],
        status: DailySummaryStatus,
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
        self.activity_type = activity_type
        self.activity_duration_minutes = activity_duration_minutes
        self.status = status
        self.updated_at = datetime.now(timezone.utc)
