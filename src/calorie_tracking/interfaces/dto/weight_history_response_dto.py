from datetime import date
from typing import List

from pydantic import BaseModel

from src.calorie_tracking.interfaces.dto.weight_history_entry_dto import WeightHistoryEntryDTO


class WeightHistoryResponseDTO(BaseModel):
    user_id: str
    start_date: date
    end_date: date
    weights: List[WeightHistoryEntryDTO]
