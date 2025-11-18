from __future__ import annotations

from typing import Optional

from src.calorie_tracking.domain.model.entities.calorie_target import CalorieTarget
from src.calorie_tracking.domain.repository.calorie_target_repository import CalorieTargetRepository
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.activity_level import ActivityLevel


class CalorieTargetService:
    def __init__(self, repository: CalorieTargetRepository):
        self.repository = repository

    def upsert_from_profile(
        self,
        *,
        patient_id: str,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: Gender,
        goal_type: GoalType | None = None,
        activity_level: ActivityLevel | None = None,
    ) -> CalorieTarget:
        calories, protein, carbs, fats = self._calculate_targets(
            weight_kg=weight_kg,
            height_cm=height_cm,
            age=age,
            gender=gender,
            goal_type=goal_type,
            activity_level=activity_level,
        )
        target = self.repository.find_by_patient_id(patient_id)
        if target:
            target.apply_update(
                calories=calories,
                protein_grams=protein,
                carb_grams=carbs,
                fat_grams=fats,
            )
        else:
            target = CalorieTarget.create(
                patient_id=patient_id,
                calories=calories,
                protein_grams=protein,
                carb_grams=carbs,
                fat_grams=fats,
            )
        return self.repository.save(target)

    def get_by_patient(self, patient_id: str) -> Optional[CalorieTarget]:
        return self.repository.find_by_patient_id(patient_id)

    def list_all(self) -> list[CalorieTarget]:
        return self.repository.list_all()

    def _calculate_targets(
        self,
        *,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: Gender,
        goal_type: GoalType | None = None,
        activity_level: ActivityLevel | None = None,
    ) -> tuple[float, float, float, float]:
        if weight_kg <= 0 or height_cm <= 0 or age <= 0:
            raise ValueError("Weight, height and age must be greater than zero.")

        gender_term = 5 if gender == Gender.MALE else -161 if gender == Gender.FEMALE else -78
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + gender_term

        activity_multiplier = 1.2
        if activity_level == ActivityLevel.LIGHT:
            activity_multiplier = 1.375
        elif activity_level == ActivityLevel.ACTIVE:
            activity_multiplier = 1.55
        elif activity_level == ActivityLevel.VERY_ACTIVE:
            activity_multiplier = 1.725
        tdee = bmr * activity_multiplier

        goal_multiplier = 1.0
        if goal_type == GoalType.BULKING:
            goal_multiplier = 1.1
        elif goal_type == GoalType.DEFINITION:
            goal_multiplier = 0.9

        calories = round(tdee * goal_multiplier)
        protein = round(weight_kg * 1.6)
        fat = round(weight_kg * 0.9)
        remaining_kcal = max(0.0, calories - (protein * 4 + fat * 9))
        carbs = round(remaining_kcal / 4)

        return calories, protein, carbs, fat
