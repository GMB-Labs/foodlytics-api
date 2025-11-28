from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


UTC_MINUS_5 = timezone(timedelta(hours=-5))


@dataclass
class NutritionistInviteCode:
    code: str
    nutritionist_id: str
    patient_id: Optional[str]
    used: bool
    created_at: datetime
    used_at: Optional[datetime]

    @classmethod
    def create(cls, *, code: str, nutritionist_id: str) -> "NutritionistInviteCode":
        now = datetime.now(UTC_MINUS_5)
        return cls(
            code=code,
            nutritionist_id=nutritionist_id,
            patient_id=None,
            used=False,
            created_at=now,
            used_at=None,
        )

    def mark_used(self, patient_id: str) -> None:
        self.patient_id = patient_id
        self.used = True
        self.used_at = datetime.now(UTC_MINUS_5)
