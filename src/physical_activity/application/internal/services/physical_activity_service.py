from datetime import date
from typing import Dict, Optional

from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import (
    DailyIntakeComparisonService,
)
from src.profile.domain.model.aggregates.profile import Profile
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.shared.infrastructure.external.physical_activity_ai_client import (
    PhysicalActivityAIClient,
)


class PhysicalActivityService:
    """
    Calcula calorías quemadas (IA o pasos) y las contrasta con calorie tracking.
    """

    def __init__(
        self,
        ai_client: PhysicalActivityAIClient,
        profile_repository: ProfileRepository,
        comparison_service: DailyIntakeComparisonService,
    ):
        self.ai_client = ai_client
        self.profile_repository = profile_repository
        self.comparison_service = comparison_service

    def _get_profile(self, user_id: str) -> Profile:
        profile = self.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found for the given user.")
        return profile

    @staticmethod
    def _profile_snapshot(profile: Profile) -> Dict:
        return {
            "user_id": profile.user_id,
            "weight_kg": profile.weight_kg,
            "height_cm": profile.height_cm,
            "age": profile.age,
            "gender": profile.gender.value if profile.gender else None,
            "activity_level": profile.activity_level.value if profile.activity_level else None,
            "goal_type": profile.goal_type.value if profile.goal_type else None,
        }

    def _contrast_with_calorie_tracking(
        self, *, patient_id: str, day: date, burned_calories: float
    ) -> Dict:
        try:
            summary = self.comparison_service.get_daily_summary(
                patient_id=patient_id, day=day
            )
            net_after_activity = summary["difference"]["calories"] + burned_calories
            return {
                "summary": summary,
                "net_after_activity": round(net_after_activity, 2),
                "error": None,
            }
        except ValueError as exc:
            return {"summary": None, "net_after_activity": None, "error": str(exc)}

    def estimate_with_ai(
        self,
        *,
        user_id: str,
        activity_type: str,
        duration_minutes: float,
        intensity: Optional[str] = None,
    ) -> Dict:
        profile = self._get_profile(user_id)
        day = date.today()
        burned_calories = self.ai_client.estimate_calories(
            weight_kg=profile.weight_kg,
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            intensity=intensity,
        )

        # Actualiza calorie tracking con el neto (calorías quemadas).
        self.comparison_service.finalize_day(
            patient_id=user_id, day=day, activity_burned=burned_calories
        )

        return {
            "activity_type": activity_type,
            "calories_burned": burned_calories,
        }

    def estimate_from_steps(
        self,
        *,
        user_id: str,
        steps: int,
        step_length_cm: Optional[float] = None,
    ) -> Dict:
        if steps <= 0:
            raise ValueError("steps must be greater than zero.")

        profile = self._get_profile(user_id)
        step_length_cm = step_length_cm or 70.0  # promedio aproximado
        day = date.today()

        distance_km = steps * step_length_cm / 100000  # cm -> km
        # Aproximación: kcal por km = peso_kg * 0.9
        calories = distance_km * profile.weight_kg * 0.9
        calories = round(calories, 2)

        self.comparison_service.finalize_day(
            patient_id=user_id, day=day, activity_burned=calories
        )

        return {
            "steps": steps,
            "calories_burned": calories,
        }

    def get_activity_by_day(self, *, user_id: str, day: date) -> Dict:
        """
        Returns burned calories and basic status for the given user and day.
        """
        # Ensure the user exists before querying summaries.
        self._get_profile(user_id)

        summary = self.comparison_service.get_daily_summary(
            patient_id=user_id, day=day
        )

        return {
            "user_id": user_id,
            "day": day,
            "activity_burned": summary.get("activity_burned", 0.0),
            "net_calories": summary.get("net_calories"),
            "status": summary.get("status"),
        }
