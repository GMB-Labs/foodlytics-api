from datetime import date

from pydantic import BaseModel

from src.calorie_tracking.interfaces.dto.macro_breakdown_no_bmi_dto import MacroBreakdownNoBmiDTO
from src.calorie_tracking.domain.model.value_objects.daily_summary_status import DailySummaryStatus


class DailyIntakeSummaryNoBmiDTO(BaseModel):
    id: str | None = None
    day: date
    patient_id: str
    target: MacroBreakdownNoBmiDTO
    consumed: MacroBreakdownNoBmiDTO
    difference: MacroBreakdownNoBmiDTO
    status: DailySummaryStatus
    activity_burned: float = 0
    net_calories: float | None = None
