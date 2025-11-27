from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class WeightHistoryEntryDTO(BaseModel):
    day: date
    weight_kg: float
    updated_at: datetime


class WeightHistoryResponseDTO(BaseModel):
    user_id: str
    start_date: date
    end_date: date
    weights: List[WeightHistoryEntryDTO]


class WeightHistoryUpsertRequestDTO(BaseModel):
    day: date
    weight_kg: float


class WeightHistoryEntryResponseDTO(BaseModel):
    user_id: str
    day: date
    weight_kg: float
    updated_at: datetime
