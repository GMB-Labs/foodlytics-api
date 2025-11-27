from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from src.calorie_tracking.domain.model.entities.daily_intake_summary import DailyIntakeSummary
from src.calorie_tracking.domain.model.value_objects.daily_summary_status import DailySummaryStatus
from src.calorie_tracking.domain.repository.daily_intake_summary_repository import DailyIntakeSummaryRepository
from src.calorie_tracking.infrastructure.persistence.sqlalchemy.models.daily_intake_summary_model import (
    DailyIntakeSummaryModel,
)


class SqlAlchemyDailyIntakeSummaryRepository(DailyIntakeSummaryRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: DailyIntakeSummaryModel) -> DailyIntakeSummary:
        return DailyIntakeSummary(
            day=model.day,
            patient_id=model.patient_id,
            target_calories=model.target_calories,
            target_protein=model.target_protein,
            target_carbs=model.target_carbs,
            target_fats=model.target_fats,
            consumed_calories=model.consumed_calories,
            consumed_protein=model.consumed_protein,
            consumed_carbs=model.consumed_carbs,
            consumed_fats=model.consumed_fats,
            activity_burned=model.activity_burned,
            status=DailySummaryStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_model(self, model: DailyIntakeSummaryModel, entity: DailyIntakeSummary) -> None:
        model.patient_id = entity.patient_id
        model.day = entity.day
        model.target_calories = entity.target_calories
        model.target_protein = entity.target_protein
        model.target_carbs = entity.target_carbs
        model.target_fats = entity.target_fats
        model.consumed_calories = entity.consumed_calories
        model.consumed_protein = entity.consumed_protein
        model.consumed_carbs = entity.consumed_carbs
        model.consumed_fats = entity.consumed_fats
        model.activity_burned = entity.activity_burned
        model.status = entity.status.value if isinstance(entity.status, DailySummaryStatus) else entity.status
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

    def find_by_patient_and_day(self, patient_id: str, day: date) -> Optional[DailyIntakeSummary]:
        model = (
            self.db.query(DailyIntakeSummaryModel)
            .filter(
                DailyIntakeSummaryModel.patient_id == patient_id,
                DailyIntakeSummaryModel.day == day,
            )
            .one_or_none()
        )
        if not model:
            return None
        return self._to_domain(model)

    def save(self, summary: DailyIntakeSummary) -> DailyIntakeSummary:
        model = (
            self.db.query(DailyIntakeSummaryModel)
            .filter(
                DailyIntakeSummaryModel.patient_id == summary.patient_id,
                DailyIntakeSummaryModel.day == summary.day,
            )
            .one_or_none()
        )
        if model is None:
            model = DailyIntakeSummaryModel()
            self._sync_model(model, summary)
            self.db.add(model)
        else:
            self._sync_model(model, summary)
        self.db.commit()
        return summary
