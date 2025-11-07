from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.profile.domain.model.aggregates.profile import Profile


class CreateProfileDTO(BaseModel):
    user_id: str = Field(..., description="Auth0 user identifier.")
    nutritionist_id: str = Field(..., description="Assigned nutritionist identifier.")
    first_name: str
    last_name: str
    age: int = Field(..., ge=0)
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    gender: str = Field(..., description="Allowed values: male, female, other.")
    goal_type: str = Field(..., description="Allowed values: definition, maintenance, bulking.")


class UpdateProfileDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)
    height_cm: Optional[float] = Field(None, gt=0)
    weight_kg: Optional[float] = Field(None, gt=0)
    gender: Optional[str] = Field(None, description="Allowed values: male, female, other.")
    goal_type: Optional[str] = Field(None, description="Allowed values: definition, maintenance, bulking.")


class ProfileResponseDTO(BaseModel):
    user_id: str
    nutritionist_id: str
    first_name: str
    last_name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: str
    goal_type: str
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
            goal_type=profile.goal_type.value,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            has_profile_picture=profile.profile_picture is not None,
        )
