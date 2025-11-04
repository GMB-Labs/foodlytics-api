from abc import ABC, abstractmethod
from typing import Optional, List
from src.shared.domain.repositories.base_repository import BaseRepository
from src.iam.domain.model.aggregates.user import User

class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_auth0_id(self, sub: str) -> Optional[User]:
        pass