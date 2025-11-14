from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.domain.repository.meal_repository import MealRepository
from src.meal_recognition.infrastructure.persistence.sqlalchemy.model.meal_model import MealModel

class SqlAlchemyMealRepository(MealRepository):
    def __init__(self, session):
        self.session = session

    def save(self, meal: Meal) -> Meal:
        model = MealModel(
            id=meal.id,
            name=meal.name,
            approximate_weight_in_grams=meal.approximate_weight_in_grams,
            kcal=meal.kcal,
            protein=meal.protein,
            carbs=meal.carbs,
            fats=meal.fats,
            uploaded_at=meal.uploaded_at,
        )
        self.session.add(model)
        self.session.commit()
        return meal
