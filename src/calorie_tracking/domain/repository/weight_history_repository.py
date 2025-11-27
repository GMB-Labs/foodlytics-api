from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List

from src.calorie_tracking.domain.model.entities.weight_history_entry import WeightHistoryEntry


class WeightHistoryRepository(ABC):
    @abstractmethod
    def upsert_for_day(
        self, *, user_id: str, day: date, weight_kg: float, updated_at: datetime
    ) -> WeightHistoryEntry:
        ...

    @abstractmethod
    def list_by_user_and_range(
        self, *, user_id: str, start_date: date, end_date: date
    ) -> List[WeightHistoryEntry]:
        ...
