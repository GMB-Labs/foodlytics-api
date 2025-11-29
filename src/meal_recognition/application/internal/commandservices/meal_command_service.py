from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.interfaces.dto.register_meal_request_dto import RegisterMealRequestDTO
from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import (
    DailyIntakeComparisonService,
)


PERU_TZ = timezone(timedelta(hours=-5))


class MealCommandService:
    def __init__(self, repository):
        self.repository = repository

    def save_recognized_meal(
        self, dto: RegisterMealRequestDTO, comparison_service: DailyIntakeComparisonService | None = None
    ):
        peru_now = datetime.now(PERU_TZ)

        meal = Meal(
            id=str(uuid4()),
            name=dto.name,
            patient_id=dto.patient_id,
            mealType=dto.meal_t,
            kcal=dto.kcal,
            protein=dto.protein,
            carbs=dto.carbs,
            fats=dto.fats,
            uploaded_at=peru_now
        )

        saved = self.repository.save(meal)

        if comparison_service:
            # Persist daily summary based on the new meal so status/net calories stay current.
            comparison_service.finalize_day(
                patient_id=dto.patient_id,
                day=peru_now.date(),
            )

        return saved
