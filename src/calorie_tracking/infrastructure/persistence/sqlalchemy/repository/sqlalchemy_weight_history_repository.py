from datetime import date, datetime
from typing import List

from sqlalchemy.orm import Session

from src.calorie_tracking.domain.model.entities.weight_history_entry import WeightHistoryEntry
from src.calorie_tracking.domain.repository.weight_history_repository import WeightHistoryRepository
from src.calorie_tracking.infrastructure.persistence.sqlalchemy.models.weight_history_model import WeightHistoryModel


class SqlAlchemyWeightHistoryRepository(WeightHistoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: WeightHistoryModel) -> WeightHistoryEntry:
        return WeightHistoryEntry(
            user_id=model.user_id,
            day=model.day,
            weight_kg=model.weight_kg,
            updated_at=model.updated_at,
        )

    def _sync_model(self, model: WeightHistoryModel, entity: WeightHistoryEntry) -> None:
        model.user_id = entity.user_id
        model.day = entity.day
        model.weight_kg = entity.weight_kg
        model.updated_at = entity.updated_at

    def upsert_for_day(
        self, *, user_id: str, day: date, weight_kg: float, updated_at: datetime
    ) -> WeightHistoryEntry:
        model = (
            self.db.query(WeightHistoryModel)
            .filter(
                WeightHistoryModel.user_id == user_id,
                WeightHistoryModel.day == day,
            )
            .one_or_none()
        )
        if model is None:
            model = WeightHistoryModel(
                user_id=user_id, day=day, weight_kg=weight_kg, updated_at=updated_at
            )
            self.db.add(model)
        else:
            model.weight_kg = weight_kg
            model.updated_at = updated_at

        self.db.commit()
        return self._to_domain(model)

    def list_by_user_and_range(
        self, *, user_id: str, start_date: date, end_date: date
    ) -> List[WeightHistoryEntry]:
        models = (
            self.db.query(WeightHistoryModel)
            .filter(
                WeightHistoryModel.user_id == user_id,
                WeightHistoryModel.day >= start_date,
                WeightHistoryModel.day <= end_date,
            )
            .order_by(WeightHistoryModel.day.asc())
            .all()
        )
        return [self._to_domain(model) for model in models]
