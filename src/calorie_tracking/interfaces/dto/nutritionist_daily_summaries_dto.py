from datetime import date
from typing import List

from pydantic import BaseModel, Field

from src.calorie_tracking.interfaces.dto.daily_intake_summary_dto import DailyIntakeSummaryDTO


class SkippedPatientDTO(BaseModel):
    patient_id: str
    reason: str


class NutritionistDailySummariesDTO(BaseModel):
    nutritionist_id: str
    day: date
    summaries: List[DailyIntakeSummaryDTO]
    skipped_patients: List[SkippedPatientDTO] = Field(default_factory=list)


class DailySummariesByDayDTO(BaseModel):
    day: date
    summaries: List[DailyIntakeSummaryDTO]
    skipped_patients: List[SkippedPatientDTO] = Field(default_factory=list)


class NutritionistDailyRangeSummariesDTO(BaseModel):
    nutritionist_id: str
    start_date: date
    end_date: date
    days: List[DailySummariesByDayDTO]
