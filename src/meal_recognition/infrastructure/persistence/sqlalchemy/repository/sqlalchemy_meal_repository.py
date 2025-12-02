from datetime import date, datetime, time, timedelta, timezone
from typing import List

from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.domain.model.valueobjects.meal_type import MealType
from src.meal_recognition.domain.repository.meal_repository import MealRepository
from src.meal_recognition.infrastructure.persistence.sqlalchemy.model.meal_model import MealModel


class SqlAlchemyMealRepository(MealRepository):
    def __init__(self, session):
        self.session = session
        self._peru_tz = timezone(timedelta(hours=-5))

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
        # Use local (UTC-5) day boundaries and compare in UTC to avoid crossing into the next/previous day.
        start_local = datetime.combine(day, time.min, tzinfo=self._peru_tz)
        end_local = start_local + timedelta(days=1)
        start_of_day = start_local.astimezone(timezone.utc)
        end_of_day = end_local.astimezone(timezone.utc)
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
        uploaded_at = model.uploaded_at
        # Normalize to Peru TZ for consistent API responses
        if uploaded_at.tzinfo is None:
            uploaded_at = uploaded_at.replace(tzinfo=timezone.utc).astimezone(self._peru_tz)
        else:
            uploaded_at = uploaded_at.astimezone(self._peru_tz)
        return Meal(
            id=model.id,
            name=model.name,
            patient_id=model.patient_id,
            mealType=meal_type,
            kcal=model.kcal,
            protein=model.protein,
            carbs=model.carbs,
            fats=model.fats,
            uploaded_at=uploaded_at,
        )
