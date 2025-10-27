from abc import ABC, abstractmethod
from typing import Optional, List

from src.iam.domain.aggregates.user import User

class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None: ...

    @abstractmethod
    def get_all_users(self) -> List[User]: ...
