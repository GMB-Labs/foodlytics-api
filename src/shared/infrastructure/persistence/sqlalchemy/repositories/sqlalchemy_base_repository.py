from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from src.shared.domain.repositories.base_repository import BaseRepository

T = TypeVar("T")

class SQLAlchemyBaseRepository(BaseRepository[T], Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def find_by_id(self, entity_id: str) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == entity_id).first()

    def save(self, entity: T) -> None:
        self.session.add(entity)

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def list_all(self) -> List[T]:
        return self.session.query(self.model).all()
