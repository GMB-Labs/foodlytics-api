from datetime import date, timedelta
from typing import Dict, Optional, List

from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import (
    DailyIntakeComparisonService,
)
from src.physical_activity.domain.model.physical_activity import PhysicalActivity
from src.physical_activity.domain.repositories.physical_activity_repository import (
    PhysicalActivityRepository,
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
        activity_repository: PhysicalActivityRepository,
    ):
        self.ai_client = ai_client
        self.profile_repository = profile_repository
        self.comparison_service = comparison_service
        self.activity_repository = activity_repository

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
        day: Optional[date] = None,
    ) -> Dict:
        profile = self._get_profile(user_id)
        day = day or date.today()
        burned_calories = self.ai_client.estimate_calories(
            weight_kg=profile.weight_kg,
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            intensity=intensity,
        )

        activity = PhysicalActivity.create(
            user_id=user_id,
            day=day,
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            intensity=intensity,
            calories_burned=burned_calories,
        )
        self.activity_repository.save(activity)

        # Actualiza calorie tracking con el neto (calorías quemadas).
        self.comparison_service.finalize_day(
            patient_id=user_id,
            day=day,
            activity_burned=burned_calories,
            activity_type=activity_type,
            activity_duration_minutes=duration_minutes,
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
        day: Optional[date] = None,
        step_length_cm: Optional[float] = None,
    ) -> Dict:
        if steps <= 0:
            raise ValueError("steps must be greater than zero.")

        profile = self._get_profile(user_id)
        step_length_cm = step_length_cm or 70.0  # promedio aproximado
        day = day or date.today()

        distance_km = steps * step_length_cm / 100000  # cm -> km
        # Aproximación: kcal por km = peso_kg * 0.9
        calories = distance_km * profile.weight_kg * 0.9
        calories = round(calories, 2)

        activity = PhysicalActivity.create(
            user_id=user_id,
            day=day,
            activity_type="steps",
            duration_minutes=None,
            intensity=None,
            calories_burned=calories,
        )
        self.activity_repository.save(activity)

        self.comparison_service.finalize_day(
            patient_id=user_id,
            day=day,
            activity_burned=calories,
            activity_type="steps",
            activity_duration_minutes=None,
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

        activities = self.activity_repository.list_by_user_and_day(user_id, day)
        total_burned = sum(a.calories_burned for a in activities)

        # Recompute summary using the actual total burned from activities.
        summary = self.comparison_service.get_daily_summary(
            patient_id=user_id, day=day, activity_burned=total_burned
        )

        return {
            "id": summary.get("id"),
            "user_id": user_id,
            "day": day,
            "activities": [
                {
                    "id": a.id,
                    "activity_type": a.activity_type,
                    "duration_minutes": a.duration_minutes,
                    "intensity": a.intensity,
                    "calories_burned": a.calories_burned,
                }
                for a in activities
            ],
            "activity_burned": total_burned,
            "net_calories": summary.get("net_calories"),
            "status": summary.get("status"),
        }

    def update_activity_by_id(
        self,
        *,
        activity_id: str,
        activity_burned: Optional[float] = None,
        activity_type: Optional[str] = None,
        activity_duration_minutes: Optional[float] = None,
    ) -> Dict:
        """
        Updates activity data by its id.
        """
        entity = self.comparison_service.update_activity_by_id(
            summary_id=activity_id,
            activity_burned=activity_burned,
            activity_type=activity_type,
            activity_duration_minutes=activity_duration_minutes,
        )
        summary = self.comparison_service.get_daily_summary(
            patient_id=entity.patient_id, day=entity.day
        )
        return {
            "id": summary.get("id"),
            "user_id": entity.patient_id,
            "day": entity.day,
            "activity_type": summary.get("activity_type"),
            "activity_duration_minutes": summary.get("activity_duration_minutes"),
            "activity_burned": summary.get("activity_burned", 0.0),
            "net_calories": summary.get("net_calories"),
            "status": summary.get("status"),
        }

    def delete_activity_by_id(self, *, activity_id: str) -> Dict:
        """
        Removes activity data by its id.
        """
        entity = self.comparison_service.remove_activity_by_id(summary_id=activity_id)
        summary = self.comparison_service.get_daily_summary(
            patient_id=entity.patient_id, day=entity.day
        )
        return {
            "id": summary.get("id"),
            "user_id": entity.patient_id,
            "day": entity.day,
            "activity_type": summary.get("activity_type"),
            "activity_duration_minutes": summary.get("activity_duration_minutes"),
            "activity_burned": summary.get("activity_burned", 0.0),
            "net_calories": summary.get("net_calories"),
            "status": summary.get("status"),
        }

    def get_activity_range(self, *, user_id: str, start_date: date, end_date: date) -> Dict:
        """
        Returns activity data for a user across a date range.
        """
        if end_date < start_date:
            raise ValueError("start_date must be on or before end_date.")

        # Validate user exists.
        self._get_profile(user_id)

        days = []
        current = start_date
        while current <= end_date:
            activities = self.activity_repository.list_by_user_and_day(user_id, current)
            total_burned = sum(a.calories_burned for a in activities)
            summary = self.comparison_service.get_daily_summary(
                patient_id=user_id, day=current, activity_burned=total_burned
            )
            days.append(
                {
                    "id": summary.get("id"),
                    "user_id": user_id,
                    "day": current,
                    "activities": [
                        {
                            "id": a.id,
                            "activity_type": a.activity_type,
                            "duration_minutes": a.duration_minutes,
                            "intensity": a.intensity,
                            "calories_burned": a.calories_burned,
                        }
                        for a in activities
                    ],
                    "activity_burned": total_burned,
                    "net_calories": summary.get("net_calories"),
                    "status": summary.get("status"),
                }
            )
            current += timedelta(days=1)

        return {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
        }
