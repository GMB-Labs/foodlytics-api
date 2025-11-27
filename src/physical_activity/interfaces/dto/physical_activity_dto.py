from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ActivityAIRequestDTO(BaseModel):
    user_id: str
    activity_type: str
    duration_minutes: float
    intensity: Optional[str] = Field(
        default=None, description="low, moderate, high (opcional, usado para el stub)."
    )


class StepsActivityRequestDTO(BaseModel):
    user_id: str
    steps: int
    step_length_cm: Optional[float] = Field(
        default=None, description="Longitud del paso en centímetros (opcional)."
    )


class ActivityCaloriesResponseDTO(BaseModel):
    activity_type: str
    calories_burned: float


class StepsCaloriesResponseDTO(BaseModel):
    steps: int
    calories_burned: float


class ActivityByDayResponseDTO(BaseModel):
    user_id: str
    day: date
    activity_type: Optional[str] = None
    activity_duration_minutes: Optional[float] = None
    activity_burned: float
    net_calories: Optional[float] = None
    status: Optional[str] = None
