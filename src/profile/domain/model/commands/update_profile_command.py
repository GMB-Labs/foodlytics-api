from dataclasses import dataclass
from typing import Optional

from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.activity_level import ActivityLevel


@dataclass(slots=True)
class UpdateProfileCommand:
    """
    Command to update an existing profile.
    """

    user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    gender: Optional[Gender] = None
    goal_type: Optional[GoalType] = None
    activity_level: Optional[ActivityLevel] = None
    desired_weight_kg: Optional[float] = None
    user_profile_completed: Optional[bool] = None

    @classmethod
    def from_primitives(
        cls,
        *,
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[int] = None,
        height_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        gender: Optional[str] = None,
        goal_type: Optional[str] = None,
        activity_level: Optional[str] = None,
        desired_weight_kg: Optional[float] = None,
        user_profile_completed: Optional[bool] = None,
    ) -> "UpdateProfileCommand":
        return cls(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            height_cm=height_cm,
            weight_kg=weight_kg,
            gender=Gender.from_string(gender) if gender else None,
            goal_type=GoalType.from_string(goal_type) if goal_type else None,
            activity_level=ActivityLevel.from_string(activity_level) if activity_level else None,
            desired_weight_kg=desired_weight_kg,
            user_profile_completed=user_profile_completed,
        )
