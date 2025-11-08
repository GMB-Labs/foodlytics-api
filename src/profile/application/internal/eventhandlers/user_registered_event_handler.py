from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from src.iam.domain.events.user_registered_event import UserRegisteredEvent
from src.iam.domain.model.value_objects.user_role import UserRole
from src.profile.application.internal.commandservices.profile_command_service import (
    ProfileCommandService,
)
from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.infrastructure.persistance.sqlalchemy.repositories.sqlalchemy_profile_repository import (
    SqlAlchemyProfileRepository,
)
from src.shared.infrastructure.persistence.sqlalchemy.engine import SessionLocal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class UserRegisteredEventHandler:
    """
    Consumes the IAM UserRegisteredEvent and ensures a profile skeleton exists.
    """

    default_first_name: str = "Pending"
    default_last_name: str = "Profile"
    default_age: int = 0
    default_height_cm: float = 0.0
    default_weight_kg: float = 0.0
    default_gender: Gender = Gender.OTHER
    default_goal: GoalType = GoalType.MAINTENANCE

    def __call__(self, event: UserRegisteredEvent) -> None:
        logger.debug("Handling UserRegisteredEvent for '%s'", event.user_id)
        session = SessionLocal()
        try:
            repository = SqlAlchemyProfileRepository(session)
            existing = repository.find_by_user_id(event.user_id)
            if existing:
                logger.debug("Profile already exists for '%s'; skipping creation.", event.user_id)
                return

            command = CreateProfileCommand(
                user_id=event.user_id,
                nutritionist_id=self._calculate_nutritionist_id(event.role, event.user_id),
                first_name=self.default_first_name,
                last_name=self.default_last_name,
                age=self.default_age,
                height_cm=self.default_height_cm,
                weight_kg=self.default_weight_kg,
                gender=self.default_gender,
                goal_type=self.default_goal,
            )

            service = ProfileCommandService(repository)
            service.create_profile(command)
            logger.info("Profile bootstrap completed for user '%s'", event.user_id)
        finally:
            session.close()

    @staticmethod
    def _calculate_nutritionist_id(role: UserRole, user_id: str) -> Optional[str]:
        """
        Nutritionists manage their own profile, so we bind them to themselves.
        Patients start without an assigned nutritionist.
        """
        if role == UserRole.NUTRITIONIST:
            return user_id
        return None
