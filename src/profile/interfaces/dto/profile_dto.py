from datetime import datetime
from pydantic import BaseModel, Field

from src.profile.domain.model.aggregates.profile import Profile


class ProfileResponseDTO(BaseModel):
    user_id: str
    nutritionist_id: str | None
    first_name: str
    last_name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: str
    goal_type: str | None = None
    activity_level: str | None = None
    desired_weight_kg: float | None = None
    user_profile_completed: bool = False
    created_at: datetime
    updated_at: datetime
    has_profile_picture: bool

    @classmethod
    def from_domain(cls, profile: Profile) -> "ProfileResponseDTO":
        return cls(
            user_id=profile.user_id,
            nutritionist_id=profile.nutritionist_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            age=profile.age,
            height_cm=profile.height_cm,
            weight_kg=profile.weight_kg,
            gender=profile.gender.value,
            goal_type=profile.goal_type.value if profile.goal_type else None,
            activity_level=profile.activity_level.value if profile.activity_level else None,
            desired_weight_kg=profile.desired_weight_kg,
            user_profile_completed=profile.user_profile_completed,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            has_profile_picture=profile.profile_picture is not None,
        )
