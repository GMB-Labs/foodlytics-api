from datetime import date, datetime, time, timedelta
from typing import List

from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.domain.model.valueobjects.meal_type import MealType
from src.meal_recognition.domain.repository.meal_repository import MealRepository
from src.meal_recognition.infrastructure.persistence.sqlalchemy.model.meal_model import MealModel


class SqlAlchemyMealRepository(MealRepository):
    def __init__(self, session):
        self.session = session

    def save(self, meal: Meal) -> Meal:
        model = MealModel(
            id=meal.id,
            name=meal.name,
            patient_id=meal.patient_id,
            meal_type=meal.mealType.value if meal.mealType else None,
            kcal=meal.kcal,
            protein=meal.protein,
            carbs=meal.carbs,
            fats=meal.fats,
            uploaded_at=meal.uploaded_at,
        )
        self.session.add(model)
        self.session.commit()
        return meal

    def get_by_day_and_user(self, day: date, user_id: str) -> List[Meal]:
        start_of_day = datetime.combine(day, time.min)
        end_of_day = start_of_day + timedelta(days=1)
        records = (
            self.session.query(MealModel)
            .filter(
                MealModel.uploaded_at >= start_of_day,
                MealModel.uploaded_at < end_of_day,
                MealModel.patient_id == user_id,
            )
            .order_by(MealModel.uploaded_at.asc())
            .all()
        )
        return [self._to_entity(record) for record in records]

    def _to_entity(self, model: MealModel) -> Meal:
        meal_type = MealType(model.meal_type) if model.meal_type else None
        return Meal(
            id=model.id,
            name=model.name,
            patient_id=model.patient_id,
            mealType=meal_type,
            kcal=model.kcal,
            protein=model.protein,
            carbs=model.carbs,
            fats=model.fats,
            uploaded_at=model.uploaded_at,
        )
