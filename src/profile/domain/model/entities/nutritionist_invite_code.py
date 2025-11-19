from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


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
        now = datetime.now(timezone.utc)
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
        self.used_at = datetime.now(timezone.utc)
