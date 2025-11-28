from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4


@dataclass
class PhysicalActivity:
    id: str
    user_id: str
    day: date
    activity_type: str
    duration_minutes: float | None
    intensity: Optional[str]
    calories_burned: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        *,
        user_id: str,
        day: date,
        activity_type: str,
        duration_minutes: float | None,
        calories_burned: float,
        intensity: Optional[str] = None,
    ) -> "PhysicalActivity":
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            day=day,
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            intensity=intensity,
            calories_burned=calories_burned,
            created_at=now,
            updated_at=now,
        )

    def apply_update(
        self,
        *,
        activity_type: Optional[str] = None,
        duration_minutes: Optional[float] = None,
        intensity: Optional[str] = None,
        calories_burned: Optional[float] = None,
    ) -> None:
        if activity_type is not None:
            self.activity_type = activity_type
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if intensity is not None:
            self.intensity = intensity
        if calories_burned is not None:
            self.calories_burned = calories_burned
        self.updated_at = datetime.now(timezone.utc)
