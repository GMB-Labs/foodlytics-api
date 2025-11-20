from typing import Optional
from pydantic import Field, BaseModel


class UpdateProfileDTO(BaseModel):
    first_name: str
    last_name: str
    age: int = Field(..., ge=0)
    gender: str = Field(..., description="Allowed values: male, female, other.")
    user_profile_completed: bool = Field(..., description="Si el usuario completó su perfil.")
    height_cm: Optional[float] = Field(None, gt=0)
    weight_kg: Optional[float] = Field(None, gt=0)
    goal_type: Optional[str] = Field(None, description="Allowed values: definition, maintenance, bulking.")
    activity_level: Optional[str] = Field(None, description="sedentary, light, active, very_active.")
    desired_weight_kg: Optional[float] = Field(None, gt=0, description="Peso objetivo opcional en kg.")
