from datetime import date, timedelta
from typing import Dict, List, Tuple

from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import (
    DailyIntakeComparisonService,
)
from src.profile.domain.repositories.profile_repository import ProfileRepository


class NutritionistDailyResultsService:
    """
    Obtains daily intake summaries for all patients assigned to a nutritionist.
    """

    def __init__(
        self,
        profile_repository: ProfileRepository,
        comparison_service: DailyIntakeComparisonService,
    ):
        self.profile_repository = profile_repository
        self.comparison_service = comparison_service

    def get_patient_summaries_for_day(
        self, *, nutritionist_id: str, day: date
    ) -> Tuple[List[Dict], List[Dict[str, str]]]:
        patients = self.profile_repository.find_patient_profile_by_nutritionist_id(
            nutritionist_id
        )
        if not patients:
            raise ValueError("No patients assigned to this nutritionist.")

        summaries: List[Dict] = []
        skipped: List[Dict[str, str]] = []

        for patient in patients:
            try:
                summary = self.comparison_service.get_daily_summary(
                    patient_id=patient.user_id, day=day
                )
                summaries.append(summary)
            except ValueError as exc:
                skipped.append({"patient_id": patient.user_id, "reason": str(exc)})

        if not summaries:
            reasons = "; ".join(
                f"{item['patient_id']}: {item['reason']}" for item in skipped
            )
            message = "No daily summaries available for assigned patients."
            if reasons:
                message = f"{message} {reasons}"
            raise ValueError(message)

        return summaries, skipped

    def get_patient_summaries_for_range(
        self, *, nutritionist_id: str, start_date: date, end_date: date
    ) -> List[Dict]:
        if end_date < start_date:
            raise ValueError("start_date must be on or before end_date.")

        patients = self.profile_repository.find_patient_profile_by_nutritionist_id(
            nutritionist_id
        )
        if not patients:
            raise ValueError("No patients assigned to this nutritionist.")

        results: List[Dict] = []
        current = start_date
        while current <= end_date:
            summaries: List[Dict] = []
            skipped: List[Dict[str, str]] = []

            for patient in patients:
                try:
                    summary = self.comparison_service.get_daily_summary(
                        patient_id=patient.user_id, day=current
                    )
                    summaries.append(summary)
                except ValueError as exc:
                    skipped.append({"patient_id": patient.user_id, "reason": str(exc)})

            results.append(
                {
                    "day": current,
                    "summaries": summaries,
                    "skipped_patients": skipped,
                }
            )
            current += timedelta(days=1)

        return results
