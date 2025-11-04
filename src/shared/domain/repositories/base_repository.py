from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    def save(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        pass