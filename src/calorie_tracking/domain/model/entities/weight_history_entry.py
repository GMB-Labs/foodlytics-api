from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone


@dataclass
class WeightHistoryEntry:
    user_id: str
    day: date
    weight_kg: float
    updated_at: datetime

    @classmethod
    def create(cls, *, user_id: str, day: date, weight_kg: float) -> "WeightHistoryEntry":
        utc_minus_5 = timezone(timedelta(hours=-5))
        return cls(
            user_id=user_id,
            day=day,
            weight_kg=weight_kg,
            updated_at=datetime.now(utc_minus_5),
        )

    def apply_update(self, *, weight_kg: float, updated_at: datetime) -> None:
        self.weight_kg = weight_kg
        self.updated_at = updated_at
