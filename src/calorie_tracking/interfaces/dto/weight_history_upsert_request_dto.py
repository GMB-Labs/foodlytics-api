from datetime import date

from pydantic import BaseModel


class WeightHistoryUpsertRequestDTO(BaseModel):
    day: date
    weight_kg: float
