from src.meal_recognition.domain.model.entities.meal import Meal
from datetime import datetime
from uuid import uuid4

from src.meal_recognition.interfaces.dto.register_meal_request_dto import RegisterMealRequestDTO


class MealCommandService:
    def __init__(self, repository):
        self.repository = repository

    def save_recognized_meal(self, dto: RegisterMealRequestDTO):

        meal = Meal(
            id=str(uuid4()),
            name=dto.name,
            approximate_weight_in_grams=dto.approximate_weight_in_grams,
            mealType=dto.meal_t,
            kcal=dto.kcal,
            protein=dto.protein,
            carbs=dto.carbs,
            fats=dto.fats,
            uploaded_at=datetime.utcnow()
        )

        return self.repository.save(meal)
