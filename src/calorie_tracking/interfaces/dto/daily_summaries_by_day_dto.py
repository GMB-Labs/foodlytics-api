from datetime import date
from typing import List

from pydantic import BaseModel, Field

from src.calorie_tracking.interfaces.dto.daily_intake_summary_dto import DailyIntakeSummaryDTO
from src.calorie_tracking.interfaces.dto.skipped_patient_dto import SkippedPatientDTO


class DailySummariesByDayDTO(BaseModel):
    day: date
    summaries: List[DailyIntakeSummaryDTO]
    skipped_patients: List[SkippedPatientDTO] = Field(default_factory=list)
