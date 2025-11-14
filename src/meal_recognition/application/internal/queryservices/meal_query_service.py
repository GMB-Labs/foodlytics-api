from datetime import date
from typing import List

from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.domain.repository.meal_repository import MealRepository


class MealQueryService:
    def __init__(self, repository: MealRepository):
        self.repository = repository

    def get_by_day(self, day: date, user_id: str) -> List[Meal]:
        return self.repository.get_by_day_and_user(day, user_id)
