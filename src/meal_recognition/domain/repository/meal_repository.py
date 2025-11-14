from abc import ABC, abstractmethod
from datetime import date
from typing import List

from src.meal_recognition.domain.model.entities.meal import Meal


class MealRepository(ABC):

    @abstractmethod
    def save(self, meal: Meal) -> Meal:
        pass

    @abstractmethod
    def get_by_day(self, day: date) -> List[Meal]:
        pass
