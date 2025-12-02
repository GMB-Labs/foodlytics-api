from datetime import date, datetime

from pydantic import BaseModel


class WeightHistoryEntryDTO(BaseModel):
    day: date
    weight_kg: float
    updated_at: datetime
