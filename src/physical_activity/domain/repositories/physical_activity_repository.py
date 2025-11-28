from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from src.physical_activity.domain.model.physical_activity import PhysicalActivity


class PhysicalActivityRepository(ABC):
    @abstractmethod
    def save(self, activity: PhysicalActivity) -> PhysicalActivity:
        ...

    @abstractmethod
    def find_by_id(self, activity_id: str) -> Optional[PhysicalActivity]:
        ...

    @abstractmethod
    def list_by_user_and_day(self, user_id: str, day: date) -> List[PhysicalActivity]:
        ...

    @abstractmethod
    def delete(self, activity: PhysicalActivity) -> None:
        ...
