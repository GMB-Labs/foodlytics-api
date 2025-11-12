from typing import List, Optional

from sqlalchemy.orm import Session

from src.profile.domain.model.aggregates.profile import Profile
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.profile_picture import ProfilePicture
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.infrastructure.persistance.sqlalchemy.model.profile_model import ProfileModel


class SqlAlchemyProfileRepository(ProfileRepository):
    """
    SQLAlchemy implementation of the ProfileRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: ProfileModel) -> Profile:
        picture: Optional[ProfilePicture] = None
        if model.profile_picture_data and model.profile_picture_mime_type:
            picture = ProfilePicture(
                image_data=model.profile_picture_data,
                mime_type=model.profile_picture_mime_type,
            )

        return Profile(
            user_id=model.user_id,
            nutritionist_id=model.nutritionist_id,
            first_name=model.first_name,
            last_name=model.last_name,
            age=model.age,
            height_cm=model.height_cm,
            weight_kg=model.weight_kg,
            gender=Gender.from_string(model.gender),
            goal_type=GoalType.from_string(model.goal_type),
            profile_picture=picture,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_model(self, model: ProfileModel, entity: Profile) -> None:
        model.id = entity.id
        model.user_id = entity.user_id
        model.nutritionist_id = entity.nutritionist_id
        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.age = entity.age
        model.height_cm = entity.height_cm
        model.weight_kg = entity.weight_kg
        model.gender = entity.gender.value
        model.goal_type = entity.goal_type.value
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

        if entity.profile_picture:
            model.profile_picture_data = entity.profile_picture.image_data
            model.profile_picture_mime_type = entity.profile_picture.mime_type
        else:
            model.profile_picture_data = None
            model.profile_picture_mime_type = None

    def find_by_id(self, entity_id: str) -> Optional[Profile]:
        model = self.db.get(ProfileModel, entity_id)
        return self._to_domain(model) if model else None

    def find_by_user_id(self, user_id: str) -> Optional[Profile]:
        model = (
            self.db.query(ProfileModel).filter(ProfileModel.user_id == user_id).one_or_none()
        )
        return self._to_domain(model) if model else None

    def find_patient_profile_by_nutritionist_id(self, nutritionist_id: str) -> List[Profile]:
        rows = (
            self.db.query(ProfileModel)
            .filter(ProfileModel.nutritionist_id == nutritionist_id)
            .all()
        )
        return [self._to_domain(row) for row in rows]

    def list_all(self) -> List[Profile]:
        rows = self.db.query(ProfileModel).all()
        return [self._to_domain(row) for row in rows]

    def save(self, profile: Profile) -> None:
        model = self.db.get(ProfileModel, profile.id)
        if model is None:
            model = ProfileModel()
            self._sync_model(model, profile)
            self.db.add(model)
        else:
            self._sync_model(model, profile)
        self.db.commit()

    def delete(self, profile: Profile) -> None:
        model = self.db.get(ProfileModel, profile.id)
        if not model:
            return
        self.db.delete(model)
        self.db.commit()


