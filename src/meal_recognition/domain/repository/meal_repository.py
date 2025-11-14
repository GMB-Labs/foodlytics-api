from abc import ABC, abstractmethod
from src.meal_recognition.domain.model.entities.meal import Meal

class MealRepository(ABC):

    @abstractmethod
    def save(self, meal: Meal) -> None:
        pass
