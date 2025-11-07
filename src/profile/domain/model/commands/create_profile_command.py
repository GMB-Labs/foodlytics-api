from dataclasses import dataclass

from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType


@dataclass(slots=True)
class CreateProfileCommand:
    """
    Command to create a new profile.
    """

    user_id: str
    nutritionist_id: str
    first_name: str
    last_name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: Gender
    goal_type: GoalType

    @classmethod
    def from_primitives(
        cls,
        *,
        user_id: str,
        nutritionist_id: str,
        first_name: str,
        last_name: str,
        age: int,
        height_cm: float,
        weight_kg: float,
        gender: str,
        goal_type: str,
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
            goal_type=GoalType.from_string(goal_type),
        )
