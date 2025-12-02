from datetime import date, datetime

from pydantic import BaseModel


class WeightHistoryEntryResponseDTO(BaseModel):
    user_id: str
    day: date
    weight_kg: float
    updated_at: datetime
