from abc import ABC, abstractmethod
from typing import Optional,Dict
from src.iam.domain.model.aggregates.user import User

class UserService(ABC):
    """
    Abstract base class for user services.
    """
    @abstractmethod
    def get_or_create_from_payload(self, payload: Dict) -> User:
        """
        Get or create a user from the given payload.
        :param payload:
        :return:
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Find a user by their ID.
        :param user_id:
        :return:
        """
        pass