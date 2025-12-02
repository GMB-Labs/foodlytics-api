from __future__ import annotations

from typing import Optional

from src.calorie_tracking.domain.model.entities.calorie_target import CalorieTarget
from src.calorie_tracking.domain.repository.calorie_target_repository import CalorieTargetRepository


class CalorieTargetQueryService:
    """
    Read-only queries for calorie targets.
    """

    def __init__(self, repository: CalorieTargetRepository):
        self.repository = repository

    def get_by_patient(self, patient_id: str) -> Optional[CalorieTarget]:
        return self.repository.find_by_patient_id(patient_id)

    def list_all(self) -> list[CalorieTarget]:
        return self.repository.list_all()
