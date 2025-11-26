from fastapi import Depends
from sqlalchemy.orm import Session

from src.nutritionist_webtools.application.internal.commandservices.task_command_service import (
    TaskCommandService,
)
from src.nutritionist_webtools.application.internal.commandservices.calendar_event_command_service import (
    CalendarEventCommandService,
)
from src.nutritionist_webtools.domain.repositories.task_repository import TaskRepository
from src.nutritionist_webtools.domain.repositories.calendar_event_repository import (
    CalendarEventRepository,
)
from src.nutritionist_webtools.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_task_repository import (
    SqlAlchemyTaskRepository,
)
from src.nutritionist_webtools.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_calendar_event_repository import (
    SqlAlchemyCalendarEventRepository,
)
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return SqlAlchemyTaskRepository(db)


def get_calendar_event_repository(db: Session = Depends(get_db)) -> CalendarEventRepository:
    return SqlAlchemyCalendarEventRepository(db)


def get_task_command_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskCommandService:
    return TaskCommandService(repository)


def get_calendar_event_command_service(
    repository: CalendarEventRepository = Depends(get_calendar_event_repository),
) -> CalendarEventCommandService:
    return CalendarEventCommandService(repository)
