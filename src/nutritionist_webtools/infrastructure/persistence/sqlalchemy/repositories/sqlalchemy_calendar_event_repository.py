from typing import List, Optional
from sqlalchemy.orm import Session

from src.nutritionist_webtools.domain.model.aggregates.calendar_event import CalendarEvent
from src.nutritionist_webtools.domain.repositories.calendar_event_repository import CalendarEventRepository
from src.nutritionist_webtools.infrastructure.persistence.sqlalchemy.models.calendar_event_model import (
    CalendarEventModel,
)


class SqlAlchemyCalendarEventRepository(CalendarEventRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: CalendarEventModel) -> CalendarEvent:
        return CalendarEvent(
            id=model.id,
            nutritionist_id=model.nutritionist_id,
            event_name=model.event_name,
            event_date=model.event_date,
            event_time=model.event_time,
        )

    def _sync_model(self, model: CalendarEventModel, entity: CalendarEvent) -> None:
        model.id = entity.id
        model.nutritionist_id = entity.nutritionist_id
        model.event_name = entity.event_name
        model.event_date = entity.event_date
        model.event_time = entity.event_time

    def list_by_nutritionist(self, nutritionist_id: str) -> List[CalendarEvent]:
        rows = (
            self.db.query(CalendarEventModel)
            .filter(CalendarEventModel.nutritionist_id == nutritionist_id)
            .order_by(CalendarEventModel.event_date, CalendarEventModel.event_time)
            .all()
        )
        return [self._to_domain(row) for row in rows]

    def find_by_id(self, event_id: str) -> Optional[CalendarEvent]:
        row = self.db.get(CalendarEventModel, event_id)
        return self._to_domain(row) if row else None

    def save(self, event: CalendarEvent) -> None:
        model = self.db.get(CalendarEventModel, event.id)
        if model is None:
            model = CalendarEventModel()
            self._sync_model(model, event)
            self.db.add(model)
        else:
            self._sync_model(model, event)
        self.db.commit()

    def delete(self, event: CalendarEvent) -> None:
        model = self.db.get(CalendarEventModel, event.id)
        if not model:
            return
        self.db.delete(model)
        self.db.commit()
