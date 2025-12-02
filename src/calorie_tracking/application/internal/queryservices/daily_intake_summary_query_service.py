from datetime import date
from typing import Dict

from src.calorie_tracking.application.internal.commandservices.daily_intake_comparison_service import (
    DailyIntakeComparisonService,
)


class DailyIntakeSummaryQueryService:
    """
    Exposes read-side daily intake summaries without coupling controllers to command commandservices.
    """

    def __init__(self, comparison_service: DailyIntakeComparisonService):
        self.comparison_service = comparison_service

    def get_daily_summary(
        self,
        *,
        patient_id: str,
        day: date,
        activity_burned: float | None = None,
        activity_type: str | None = None,
        activity_duration_minutes: float | None = None,
    ) -> Dict:
        return self.comparison_service.get_daily_summary(
            patient_id=patient_id,
            day=day,
            activity_burned=activity_burned,
            activity_type=activity_type,
            activity_duration_minutes=activity_duration_minutes,
        )
