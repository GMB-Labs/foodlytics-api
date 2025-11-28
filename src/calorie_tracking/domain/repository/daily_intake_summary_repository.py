from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from src.calorie_tracking.domain.model.entities.daily_intake_summary import DailyIntakeSummary


class DailyIntakeSummaryRepository(ABC):
    @abstractmethod
    def find_by_id(self, summary_id: str) -> Optional[DailyIntakeSummary]:
        ...

    @abstractmethod
    def find_by_patient_and_day(self, patient_id: str, day: date) -> Optional[DailyIntakeSummary]:
        pass

    @abstractmethod
    def save(self, summary: DailyIntakeSummary) -> DailyIntakeSummary:
        pass
