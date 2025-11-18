from __future__ import annotations

import logging
from dataclasses import dataclass

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.infrastructure.persistence.sqlalchemy.repository import SqlAlchemyCalorieTargetRepository
from src.iam.infrastructure.persistence.sqlalchemy.repositories.user_repository_impl import SqlAlchemyUserRepository
from src.profile.domain.events import ProfileUpdatedEvent
from src.shared.infrastructure.persistence.sqlalchemy.engine import SessionLocal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ProfileUpdatedEventHandler:
    """
    Rebuilds calorie targets whenever a profile is created or updated.
    """

    def __call__(self, event: ProfileUpdatedEvent) -> None:
        session = SessionLocal()
        try:
            user_repo = SqlAlchemyUserRepository(session)
            user = user_repo.find_by_id(event.user_id)
            if user and not user.is_patient():
                logger.debug(
                    "Skipping calorie target update for non-patient '%s'", event.user_id
                )
                return

            repository = SqlAlchemyCalorieTargetRepository(session)
            service = CalorieTargetService(repository)
            service.upsert_from_profile(
                patient_id=event.user_id,
                weight_kg=event.weight_kg,
                height_cm=event.height_cm,
                age=event.age,
                gender=event.gender,
                goal_type=event.goal_type,
                activity_level=event.activity_level,
            )
            logger.info("Calorie target updated for patient '%s'", event.user_id)
        except ValueError as exc:
            logger.warning(
                "Could not update calorie target for '%s': %s", event.user_id, exc
            )
        finally:
            session.close()
