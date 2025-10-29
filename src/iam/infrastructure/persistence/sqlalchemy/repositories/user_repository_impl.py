from typing import Optional, List

from sqlalchemy.orm import Session

from src.iam.domain.model.aggregates.user import User, UserRole
from src.iam.domain.repositories.user_repository import UserRepository
from src.iam.infrastructure.persistence.sqlalchemy.models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, m: UserModel) -> User:
        # Si role viene en string de .name, mapeamos a enum
        try:
            role = UserRole[m.role]
        except Exception:
            # fallback: si llega en minúsculas
            role = UserRole.NUTRITIONIST if m.role.lower() == "nutritionist" else UserRole.PATIENT

        return User(
            id=m.id,
            username=m.username,
            email=m.email,
            role=role,
            scopes=m.scopes or [],
            permissions=m.permissions or [],
        )

    def _sync_model(self, m: UserModel, e: User) -> None:
        m.username = e.username
        m.email = e.email
        m.role = e.role.name
        m.scopes = list(e.scopes or [])
        m.permissions = list(e.permissions or [])

    def find_by_id(self, entity_id: str) -> Optional[User]:
        m = self.db.get(UserModel, entity_id)
        return self._to_domain(m) if m else None

    def find_by_email(self, email: str) -> Optional[User]:
        m = self.db.query(UserModel).filter(UserModel.email == email).one_or_none()
        return self._to_domain(m) if m else None

    def find_by_auth0_id(self, sub: str) -> Optional[User]:
        # En este diseño, id == sub
        return self.find_by_id(sub)

    def list_all(self) -> List[User]:
        rows = self.db.query(UserModel).all()
        return [self._to_domain(m) for m in rows]

    def save(self, entity: User) -> None:
        m = self.db.get(UserModel, entity.id)
        if m:
            self._sync_model(m, entity)
        else:
            m = UserModel(
                id=entity.id,
                username=entity.username,
                email=entity.email,
                role=entity.role.name,
                scopes=list(entity.scopes or []),
                permissions=list(entity.permissions or []),
            )
            self.db.add(m)
        self.db.commit()

    def delete(self, entity: User) -> None:
        m = self.db.get(UserModel, entity.id)
        if m:
            self.db.delete(m)
            self.db.commit()