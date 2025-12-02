from datetime import date
from typing import List

from pydantic import BaseModel

from src.calorie_tracking.interfaces.dto.daily_summaries_by_day_dto import DailySummariesByDayDTO


class NutritionistDailyRangeSummariesDTO(BaseModel):
    nutritionist_id: str
    start_date: date
    end_date: date
    days: List[DailySummariesByDayDTO]
