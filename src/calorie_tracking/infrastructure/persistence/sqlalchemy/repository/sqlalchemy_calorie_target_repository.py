from typing import Optional

from sqlalchemy.orm import Session

from src.calorie_tracking.domain.model.entities.calorie_target import CalorieTarget
from src.calorie_tracking.domain.repository.calorie_target_repository import CalorieTargetRepository
from src.calorie_tracking.infrastructure.persistence.sqlalchemy.models.calorie_target_model import CalorieTargetModel


class SqlAlchemyCalorieTargetRepository(CalorieTargetRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: CalorieTargetModel) -> CalorieTarget:
        return CalorieTarget(
            patient_id=model.patient_id,
            calories=model.calories,
            protein_grams=model.protein_grams,
            carb_grams=model.carb_grams,
            fat_grams=model.fat_grams,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_model(self, model: CalorieTargetModel, entity: CalorieTarget) -> None:
        model.patient_id = entity.patient_id
        model.calories = entity.calories
        model.protein_grams = entity.protein_grams
        model.carb_grams = entity.carb_grams
        model.fat_grams = entity.fat_grams
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

    def find_by_patient_id(self, patient_id: str) -> Optional[CalorieTarget]:
        model = self.db.get(CalorieTargetModel, patient_id)
        if not model:
            return None
        return self._to_domain(model)

    def save(self, target: CalorieTarget) -> CalorieTarget:
        model = self.db.get(CalorieTargetModel, target.patient_id)
        if model is None:
            model = CalorieTargetModel()
            self._sync_model(model, target)
            self.db.add(model)
        else:
            self._sync_model(model, target)
        self.db.commit()
        return target

    def list_all(self) -> list[CalorieTarget]:
        rows = self.db.query(CalorieTargetModel).all()
        return [self._to_domain(row) for row in rows]
