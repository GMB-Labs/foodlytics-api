from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timezone

from src.calorie_tracking.infrastructure.persistence.sqlalchemy.repository import (
    SqlAlchemyWeightHistoryRepository,
)
from src.profile.domain.events import ProfileUpdatedEvent
from src.shared.infrastructure.persistence.sqlalchemy.engine import SessionLocal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class WeightHistoryEventHandler:
    """
    Records the latest weight per day whenever a profile is updated.
    """

    def __call__(self, event: ProfileUpdatedEvent) -> None:
        session = SessionLocal()
        try:
            repo = SqlAlchemyWeightHistoryRepository(session)
            day = event.occurred_on.astimezone(timezone.utc).date()
            repo.upsert_for_day(
                user_id=event.user_id,
                day=day,
                weight_kg=event.weight_kg,
                updated_at=event.occurred_on,
            )
            logger.info("Weight history updated for '%s' on %s", event.user_id, day)
        except Exception:  # pragma: no cover - log but keep processing
            logger.exception(
                "Could not persist weight history for user '%s'", event.user_id
            )
        finally:
            session.close()
