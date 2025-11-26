from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.iam.domain.model.aggregates.user import User, UserRole
from src.iam.domain.repositories.user_repository import UserRepository
from src.iam.infrastructure.persistence.sqlalchemy.models.user_model import UserModel

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, m: UserModel) -> User:
        try:
            role = UserRole[m.role]
        except Exception:
            role = UserRole.NUTRITIONIST if (m.role or "").lower() == "nutritionist" else UserRole.PATIENT

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
        if not email:
            return None
        m = self.db.query(UserModel).filter(UserModel.email == email).one_or_none()
        return self._to_domain(m) if m else None

    def find_by_auth0_id(self, sub: str) -> Optional[User]:
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
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()

            # Reintenta estrategia: si choca por email/username, actualiza existente por email
            existing = self.db.query(UserModel).filter(UserModel.email == entity.email).one_or_none()
            if existing:
                # Si el PK no coincide (sub distinto) y aún no tienes FKs, puedes re-key:
                # borrar y reinsertar con el nuevo id. Si ya hay FKs, mejor aplicar "account linking" en Auth0.
                self.db.delete(existing)
                self.db.flush()
                self.db.add(UserModel(
                    id=entity.id,
                    username=entity.username,
                    email=entity.email,
                    role=entity.role.name,
                    scopes=list(entity.scopes or []),
                    permissions=list(entity.permissions or []),
                ))
                self.db.commit()
            else:
                raise

    def delete(self, entity: User) -> None:
        m = self.db.get(UserModel, entity.id)
        if m:
            self.db.delete(m)
            self.db.commit()
