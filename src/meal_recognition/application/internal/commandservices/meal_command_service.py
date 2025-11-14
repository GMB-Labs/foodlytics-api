from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.domain.repository.meal_repository import MealRepository

class MealCommandService:

    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    def save_recognized_meal(self, dto):
        meal = Meal.create(
            name=dto.name,
            approx_w=dto.approximate_weight_in_grams,
            kcal=dto.kcal,
            protein=dto.protein,
            carbs=dto.carbs,
            fats=dto.fats,
        )
        self.meal_repository.save(meal)
        return meal
