from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class ActivityAIRequestDTO(BaseModel):
    user_id: str
    activity_type: str
    duration_minutes: float
    day: Optional[date] = Field(default=None, description="Día de la actividad (opcional, default hoy).")
    intensity: Optional[str] = Field(
        default=None, description="low, moderate, high (opcional, usado para el stub)."
    )


class StepsActivityRequestDTO(BaseModel):
    user_id: str
    steps: int
    day: Optional[date] = Field(default=None, description="Día de la actividad (opcional, default hoy).")
    step_length_cm: Optional[float] = Field(
        default=None, description="Longitud del paso en centímetros (opcional)."
    )


class ActivityCaloriesResponseDTO(BaseModel):
    activity_type: str
    calories_burned: float


class StepsCaloriesResponseDTO(BaseModel):
    steps: int
    calories_burned: float


class PhysicalActivityItemDTO(BaseModel):
    id: str
    activity_type: str
    duration_minutes: Optional[float] = None
    intensity: Optional[str] = None
    calories_burned: float


class ActivityByDayResponseDTO(BaseModel):
    id: Optional[str] = None
    user_id: str
    day: date
    activities: List[PhysicalActivityItemDTO] = []
    activity_burned: float
    net_calories: Optional[float] = None
    status: Optional[str] = None


class ActivityRangeResponseDTO(BaseModel):
    user_id: str
    start_date: date
    end_date: date
    days: List[ActivityByDayResponseDTO]


class ActivityUpdateRequestDTO(BaseModel):
    activity_burned: Optional[float] = None
    activity_type: Optional[str] = None
    activity_duration_minutes: Optional[float] = None
