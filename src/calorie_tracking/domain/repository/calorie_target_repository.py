from abc import ABC, abstractmethod
from typing import Optional

from src.calorie_tracking.domain.model.entities.calorie_target import CalorieTarget


class CalorieTargetRepository(ABC):

    @abstractmethod
    def find_by_patient_id(self, patient_id: str) -> Optional[CalorieTarget]:
        pass

    @abstractmethod
    def save(self, target: CalorieTarget) -> CalorieTarget:
        pass

    @abstractmethod
    def list_all(self) -> list[CalorieTarget]:
        pass
