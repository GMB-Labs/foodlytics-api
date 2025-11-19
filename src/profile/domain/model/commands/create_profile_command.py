from dataclasses import dataclass
from typing import Optional

from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.activity_level import ActivityLevel


@dataclass(slots=True)
class CreateProfileCommand:
    """
    Command to create a new profile.
    """

    user_id: str
    nutritionist_id: Optional[str]
    first_name: str
    last_name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: Gender
    goal_type: GoalType | None
    activity_level: ActivityLevel | None = None
    desired_weight_kg: float | None = None
    user_profile_completed: bool = False

    @classmethod
    def from_primitives(
        cls,
        *,
        user_id: str,
        nutritionist_id: Optional[str],
        first_name: str,
        last_name: str,
        age: int,
        height_cm: float,
        weight_kg: float,
        gender: str,
        goal_type: str | None,
        activity_level: str | None = None,
        desired_weight_kg: float | None = None,
        user_profile_completed: bool = False,
    ) -> "CreateProfileCommand":
        """
        Helper factory that accepts raw strings (e.g. payloads) and converts them into value objects.
        """
        return cls(
            user_id=user_id,
            nutritionist_id=nutritionist_id,
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
