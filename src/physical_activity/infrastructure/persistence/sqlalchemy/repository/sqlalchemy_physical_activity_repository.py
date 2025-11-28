from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from src.physical_activity.domain.model.physical_activity import PhysicalActivity
from src.physical_activity.domain.repositories.physical_activity_repository import (
    PhysicalActivityRepository,
)
from src.physical_activity.infrastructure.persistence.sqlalchemy.models.physical_activity_model import (
    PhysicalActivityModel,
)


class SqlAlchemyPhysicalActivityRepository(PhysicalActivityRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: PhysicalActivityModel) -> PhysicalActivity:
        return PhysicalActivity(
            id=model.id,
            user_id=model.user_id,
            day=model.day,
            activity_type=model.activity_type,
            duration_minutes=model.duration_minutes,
            intensity=model.intensity,
            calories_burned=model.calories_burned,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_model(self, model: PhysicalActivityModel, entity: PhysicalActivity) -> None:
        model.id = entity.id
        model.user_id = entity.user_id
        model.day = entity.day
        model.activity_type = entity.activity_type
        model.duration_minutes = entity.duration_minutes
        model.intensity = entity.intensity
        model.calories_burned = entity.calories_burned
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

    def save(self, activity: PhysicalActivity) -> PhysicalActivity:
        model = self.db.query(PhysicalActivityModel).filter(PhysicalActivityModel.id == activity.id).one_or_none()
        if model is None:
            model = PhysicalActivityModel()
            self._sync_model(model, activity)
            self.db.add(model)
        else:
            self._sync_model(model, activity)
        self.db.commit()
        return activity

    def find_by_id(self, activity_id: str) -> Optional[PhysicalActivity]:
        model = (
            self.db.query(PhysicalActivityModel)
            .filter(PhysicalActivityModel.id == activity_id)
            .one_or_none()
        )
        if not model:
            return None
        return self._to_domain(model)

    def list_by_user_and_day(self, user_id: str, day: date) -> List[PhysicalActivity]:
        models = (
            self.db.query(PhysicalActivityModel)
            .filter(PhysicalActivityModel.user_id == user_id, PhysicalActivityModel.day == day)
            .order_by(PhysicalActivityModel.created_at.asc())
            .all()
        )
        return [self._to_domain(model) for model in models]

    def delete(self, activity: PhysicalActivity) -> None:
        self.db.query(PhysicalActivityModel).filter(PhysicalActivityModel.id == activity.id).delete()
        self.db.commit()
