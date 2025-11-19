from typing import Optional

from sqlalchemy.orm import Session

from src.profile.domain.model.entities.nutritionist_invite_code import NutritionistInviteCode
from src.profile.domain.repositories.nutritionist_invite_code_repository import (
    NutritionistInviteCodeRepository,
)
from src.profile.infrastructure.persistance.sqlalchemy.model.nutritionist_invite_code_model import (
    NutritionistInviteCodeModel,
)


class SqlAlchemyNutritionistInviteCodeRepository(NutritionistInviteCodeRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: NutritionistInviteCodeModel) -> NutritionistInviteCode:
        return NutritionistInviteCode(
            code=model.code,
            nutritionist_id=model.nutritionist_id,
            patient_id=model.patient_id,
            used=model.used,
            created_at=model.created_at,
            used_at=model.used_at,
        )

    def _sync_model(self, model: NutritionistInviteCodeModel, entity: NutritionistInviteCode) -> None:
        model.code = entity.code
        model.nutritionist_id = entity.nutritionist_id
        model.patient_id = entity.patient_id
        model.used = entity.used
        model.created_at = entity.created_at
        model.used_at = entity.used_at

    def save(self, code: NutritionistInviteCode) -> NutritionistInviteCode:
        model = self.db.get(NutritionistInviteCodeModel, code.code)
        if model is None:
            model = NutritionistInviteCodeModel()
            self._sync_model(model, code)
            self.db.add(model)
        else:
            self._sync_model(model, code)
        self.db.commit()
        return code

    def find_by_code(self, code: str) -> Optional[NutritionistInviteCode]:
        model = self.db.get(NutritionistInviteCodeModel, code)
        return self._to_domain(model) if model else None

    def find_active_by_nutritionist(self, nutritionist_id: str) -> Optional[NutritionistInviteCode]:
        model = (
            self.db.query(NutritionistInviteCodeModel)
            .filter(
                NutritionistInviteCodeModel.nutritionist_id == nutritionist_id,
                NutritionistInviteCodeModel.used.is_(False),
            )
            .order_by(NutritionistInviteCodeModel.created_at.desc())
            .first()
        )
        return self._to_domain(model) if model else None
