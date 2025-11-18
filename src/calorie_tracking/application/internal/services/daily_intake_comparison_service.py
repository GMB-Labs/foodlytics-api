from datetime import date
from typing import Dict, List

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.domain.model.entities.daily_intake_summary import DailyIntakeSummary
from src.calorie_tracking.domain.repository.daily_intake_summary_repository import DailyIntakeSummaryRepository
from src.meal_recognition.domain.model.entities.meal import Meal
from src.meal_recognition.domain.repository.meal_repository import MealRepository


class DailyIntakeComparisonService:
    """
    Aggregates meals per day and compares them against the patient's calorie target.
    """

    def __init__(
        self,
        meal_repository: MealRepository,
        target_service: CalorieTargetService,
        summary_repository: DailyIntakeSummaryRepository | None = None,
    ):
        self.meal_repository = meal_repository
        self.target_service = target_service
        self.summary_repository = summary_repository

    def get_daily_summary(self, *, patient_id: str, day: date) -> Dict:
        target = self.target_service.get_by_patient(patient_id)
        if not target:
            raise ValueError("Calorie target not found for this patient.")

        meals: List[Meal] = self.meal_repository.get_by_day_and_user(day, patient_id)

        totals = self._aggregate_meals(meals)
        diff = {
            "calories": target.calories - totals["calories"],
            "protein": target.protein_grams - totals["protein"],
            "carbs": target.carb_grams - totals["carbs"],
            "fats": target.fat_grams - totals["fats"],
        }

        status = "within_target"
        if totals["calories"] > target.calories:
            status = "over_target"
        elif totals["calories"] < target.calories * 0.9:
            status = "under_target"

        return {
            "day": day,
            "patient_id": patient_id,
            "target": {
                "calories": target.calories,
                "protein": target.protein_grams,
                "carbs": target.carb_grams,
                "fats": target.fat_grams,
            },
            "consumed": totals,
            "difference": diff,
            "status": status,
        }

    def finalize_day(self, *, patient_id: str, day: date) -> DailyIntakeSummary:
        if not self.summary_repository:
            raise RuntimeError("DailyIntakeSummaryRepository is not configured.")

        summary_dict = self.get_daily_summary(patient_id=patient_id, day=day)
        target = summary_dict["target"]
        consumed = summary_dict["consumed"]

        entity = self.summary_repository.find_by_patient_and_day(patient_id, day)
        if entity:
            entity.apply_update(
                target_calories=target["calories"],
                target_protein=target["protein"],
                target_carbs=target["carbs"],
                target_fats=target["fats"],
                consumed_calories=consumed["calories"],
                consumed_protein=consumed["protein"],
                consumed_carbs=consumed["carbs"],
                consumed_fats=consumed["fats"],
                status=summary_dict["status"],
            )
        else:
            entity = DailyIntakeSummary.create(
                day=day,
                patient_id=patient_id,
                target_calories=target["calories"],
                target_protein=target["protein"],
                target_carbs=target["carbs"],
                target_fats=target["fats"],
                consumed_calories=consumed["calories"],
                consumed_protein=consumed["protein"],
                consumed_carbs=consumed["carbs"],
                consumed_fats=consumed["fats"],
                status=summary_dict["status"],
            )

        return self.summary_repository.save(entity)

    @staticmethod
    def _aggregate_meals(meals: List[Meal]) -> Dict[str, float]:
        totals = {
            "calories": 0.0,
            "protein": 0.0,
            "carbs": 0.0,
            "fats": 0.0,
        }
        for meal in meals:
            totals["calories"] += meal.kcal or 0
            totals["protein"] += meal.protein or 0
            totals["carbs"] += meal.carbs or 0
            totals["fats"] += meal.fats or 0

        # Round to whole units for consistency with targets.
        return {k: round(v) for k, v in totals.items()}
