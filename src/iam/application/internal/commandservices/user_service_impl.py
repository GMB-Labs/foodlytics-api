from typing import Optional, Dict
from src.iam.domain.model.aggregates.user import User as User
from src.iam.domain.repositories.user_repository import UserRepository
from src.iam.domain.services.user_service import UserService


class UserServiceImpl(UserService):
    """
    Implementation of the UserService interface for managing users.
    """


    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_or_create_from_payload(self, payload: Dict) -> User:
        """
        Get or create a user from the given payload.
        :param payload:
        :return:
        """
        sub = payload.get("sub")
        email = payload.get("email")

        user = self.user_repository.find_by_auth0_id(sub)
        if not user and email:
            user = self.user_repository.find_by_email(email)

        if not user:
            user = User.from_auth0_payload(payload)
            self.user_repository.save(user)
            return user

        updated = User.from_auth0_payload(payload)
        updated.username = user.username or updated.username

        if user.id != updated.id:
            self.user_repository.delete(user)

        self.user_repository.save(updated)
        return updated

    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Find a user by their ID.
        :param user_id:
        :return:
        """
        return self.user_repository.find_by_id(user_id)
