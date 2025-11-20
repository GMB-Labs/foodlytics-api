from dataclasses import dataclass
from typing import Optional

from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.activity_level import ActivityLevel


@dataclass(slots=True)
class UpdateProfileCommand:
    """
    Command to update an existing profile.
    Required fields: first_name, last_name, age, gender, user_profile_completed.
    """

    user_id: str
    first_name: str
    last_name: str
    age: int
    gender: Gender
    user_profile_completed: bool
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    goal_type: Optional[GoalType] = None
    activity_level: Optional[ActivityLevel] = None
    desired_weight_kg: Optional[float] = None

    @classmethod
    def from_primitives(
        cls,
        *,
        user_id: str,
        first_name: str,
        last_name: str,
        age: int,
        height_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        gender: str,
        goal_type: Optional[str] = None,
        activity_level: Optional[str] = None,
        desired_weight_kg: Optional[float] = None,
        user_profile_completed: bool = False,
    ) -> "UpdateProfileCommand":
        return cls(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            height_cm=height_cm,
            weight_kg=weight_kg,
            gender=Gender.from_string(gender),
            goal_type=GoalType.from_string(goal_type) if goal_type else None,
            activity_level=ActivityLevel.from_string(activity_level) if activity_level else None,
            desired_weight_kg=desired_weight_kg,
            user_profile_completed=user_profile_completed,
        )
