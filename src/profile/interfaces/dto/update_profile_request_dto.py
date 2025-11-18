from typing import Optional
from pydantic import Field, BaseModel

class UpdateProfileDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)
    height_cm: Optional[float] = Field(None, gt=0)
    weight_kg: Optional[float] = Field(None, gt=0)
    gender: Optional[str] = Field(None, description="Allowed values: male, female, other.")
    goal_type: Optional[str] = Field(None, description="Allowed values: definition, maintenance, bulking.")
    activity_level: Optional[str] = Field(None, description="sedentary, light, active, very_active.")
    desired_weight_kg: Optional[float] = Field(None, gt=0, description="Peso objetivo opcional en kg.")

