from datetime import date
from typing import Dict, List

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.domain.model.entities.daily_intake_summary import DailyIntakeSummary
from src.calorie_tracking.domain.model.value_objects.daily_summary_status import DailySummaryStatus
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
        profile_repository=None,
    ):
        self.meal_repository = meal_repository
        self.target_service = target_service
        self.summary_repository = summary_repository
        self.profile_repository = profile_repository

    def _current_activity_burned(self, patient_id: str, day: date) -> float:
        if not self.summary_repository:
            return 0.0
        existing = self.summary_repository.find_by_patient_and_day(patient_id, day)
        if not existing:
            return 0.0
        return getattr(existing, "activity_burned", 0.0) or 0.0

    def get_daily_summary(
        self,
        *,
        patient_id: str,
        day: date,
        activity_burned: float | None = None,
        activity_type: str | None = None,
        activity_duration_minutes: float | None = None,
    ) -> Dict:
        target = self.target_service.get_by_patient(patient_id)
        if not target:
            raise ValueError("Calorie target not found for this patient.")

        existing = None
        if activity_burned is None and self.summary_repository:
            existing = self.summary_repository.find_by_patient_and_day(patient_id, day)
            activity_burned = getattr(existing, "activity_burned", 0.0) or 0.0
        elif activity_burned is None:
            activity_burned = 0.0

        if existing is None and self.summary_repository:
            existing = self.summary_repository.find_by_patient_and_day(patient_id, day)

        existing_type = getattr(existing, "activity_type", None) if existing else None
        existing_duration = (
            getattr(existing, "activity_duration_minutes", None) if existing else None
        )

        meals: List[Meal] = self.meal_repository.get_by_day_and_user(day, patient_id)

        totals = self._aggregate_meals(meals)
        net_calories = max(totals["calories"] - (activity_burned or 0), 0)
        diff_calories = target.calories - net_calories
        diff = {
            "calories": diff_calories,
            "protein": target.protein_grams - totals["protein"],
            "carbs": target.carb_grams - totals["carbs"],
            "fats": target.fat_grams - totals["fats"],
        }

        bmi = self._calculate_bmi(patient_id)

        status = DailySummaryStatus.WITHIN_TARGET
        if net_calories > target.calories:
            status = DailySummaryStatus.OVER_TARGET
        elif net_calories < target.calories * 0.9:
            status = DailySummaryStatus.UNDER_TARGET

        return {
            "day": day,
            "patient_id": patient_id,
            "target": {
                "calories": target.calories,
                "protein": target.protein_grams,
                "carbs": target.carb_grams,
                "fats": target.fat_grams,
                "bmi": bmi,
            },
            "consumed": totals,
            "difference": diff,
            "activity_burned": activity_burned,
            "activity_type": activity_type or existing_type,
            "activity_duration_minutes": activity_duration_minutes or existing_duration,
            "net_calories": net_calories,
            "status": status.value,
        }

    def _calculate_bmi(self, patient_id: str) -> float | None:
        if not self.profile_repository:
            return None
        profile = self.profile_repository.find_by_user_id(patient_id)
        if not profile or not profile.weight_kg or not profile.height_cm:
            return None
        if profile.height_cm <= 0 or profile.weight_kg <= 0:
            return None
        height_m = profile.height_cm / 100
        return round(profile.weight_kg / (height_m ** 2), 2)

    def finalize_day(
        self,
        *,
        patient_id: str,
        day: date,
        activity_burned: float = 0.0,
        activity_type: str | None = None,
        activity_duration_minutes: float | None = None,
    ) -> DailyIntakeSummary:
        if not self.summary_repository:
            raise RuntimeError("DailyIntakeSummaryRepository is not configured.")

        existing_burn = self._current_activity_burned(patient_id, day)
        total_activity_burned = existing_burn + activity_burned

        summary_dict = self.get_daily_summary(
            patient_id=patient_id,
            day=day,
            activity_burned=total_activity_burned,
            activity_type=activity_type,
            activity_duration_minutes=activity_duration_minutes,
        )
        target = summary_dict["target"]
        consumed = summary_dict["consumed"]
        net_calories = summary_dict.get("net_calories", consumed["calories"])

        entity = self.summary_repository.find_by_patient_and_day(patient_id, day)
        status = DailySummaryStatus(summary_dict["status"])

        if entity:
            entity.apply_update(
                target_calories=target["calories"],
                target_protein=target["protein"],
                target_carbs=target["carbs"],
                target_fats=target["fats"],
                consumed_calories=net_calories,
                consumed_protein=consumed["protein"],
                consumed_carbs=consumed["carbs"],
                consumed_fats=consumed["fats"],
                activity_burned=total_activity_burned,
                activity_type=summary_dict.get("activity_type"),
                activity_duration_minutes=summary_dict.get("activity_duration_minutes"),
                status=status,
            )
        else:
            entity = DailyIntakeSummary.create(
                day=day,
                patient_id=patient_id,
                target_calories=target["calories"],
                target_protein=target["protein"],
                target_carbs=target["carbs"],
                target_fats=target["fats"],
                consumed_calories=net_calories,
                consumed_protein=consumed["protein"],
                consumed_carbs=consumed["carbs"],
                consumed_fats=consumed["fats"],
                activity_burned=total_activity_burned,
                activity_type=summary_dict.get("activity_type"),
                activity_duration_minutes=summary_dict.get("activity_duration_minutes"),
                status=status,
            )

        return self.summary_repository.save(entity)

    def remove_activity(
        self, *, patient_id: str, day: date
    ) -> DailyIntakeSummary:
        """
        Removes activity data for the given day (resets activity_burned/type/duration to zero/None).
        """
        if not self.summary_repository:
            raise RuntimeError("DailyIntakeSummaryRepository is not configured.")

        entity = self.summary_repository.find_by_patient_and_day(patient_id, day)
        if not entity:
            raise ValueError("Daily summary not found for this patient and day.")

        summary_dict = self.get_daily_summary(
            patient_id=patient_id,
            day=day,
            activity_burned=0.0,
            activity_type=None,
            activity_duration_minutes=None,
        )
        target = summary_dict["target"]
        consumed = summary_dict["consumed"]
        net_calories = summary_dict.get("net_calories", consumed["calories"])
        status = DailySummaryStatus(summary_dict["status"])

        entity.apply_update(
            target_calories=target["calories"],
            target_protein=target["protein"],
            target_carbs=target["carbs"],
            target_fats=target["fats"],
            consumed_calories=net_calories,
            consumed_protein=consumed["protein"],
            consumed_carbs=consumed["carbs"],
            consumed_fats=consumed["fats"],
            activity_burned=0.0,
            activity_type=None,
            activity_duration_minutes=None,
            status=status,
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
