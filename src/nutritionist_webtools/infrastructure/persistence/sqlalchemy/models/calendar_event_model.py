from sqlalchemy import Column, Date, String, Time, Index

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class CalendarEventModel(Base):
    __tablename__ = "nutritionist_calendar_events"

    id = Column(String(50), primary_key=True)
    nutritionist_id = Column(String(50), index=True, nullable=False)
    event_name = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=False)


Index("idx_calendar_events_nutritionist_id", CalendarEventModel.nutritionist_id)
