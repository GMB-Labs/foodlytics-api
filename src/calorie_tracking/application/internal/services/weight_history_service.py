from datetime import date, datetime, timezone
from typing import Dict

from src.calorie_tracking.domain.repository.weight_history_repository import WeightHistoryRepository
from src.profile.domain.repositories.profile_repository import ProfileRepository


class WeightHistoryService:
    """
    Retrieves weight changes per day for a given user within a date range.
    """

    def __init__(
        self,
        weight_history_repository: WeightHistoryRepository,
        profile_repository: ProfileRepository,
    ):
        self.weight_history_repository = weight_history_repository
        self.profile_repository = profile_repository

    def _ensure_user_exists(self, user_id: str) -> None:
        profile = self.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found for this user.")

    def get_history(self, *, user_id: str, start_date: date, end_date: date) -> Dict:
        if end_date < start_date:
            raise ValueError("start_date must be on or before end_date.")

        self._ensure_user_exists(user_id)

        entries = self.weight_history_repository.list_by_user_and_range(
            user_id=user_id, start_date=start_date, end_date=end_date
        )

        return {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "weights": [
                {
                    "day": entry.day,
                    "weight_kg": entry.weight_kg,
                    "updated_at": entry.updated_at,
                }
                for entry in entries
            ],
        }

    def record_weight(self, *, user_id: str, day: date, weight_kg: float) -> Dict:
        if weight_kg <= 0:
            raise ValueError("weight_kg must be greater than zero.")

        self._ensure_user_exists(user_id)

        entry = self.weight_history_repository.upsert_for_day(
            user_id=user_id,
            day=day,
            weight_kg=weight_kg,
            updated_at=datetime.now(timezone.utc),
        )

        return {
            "user_id": entry.user_id,
            "day": entry.day,
            "weight_kg": entry.weight_kg,
            "updated_at": entry.updated_at,
        }
