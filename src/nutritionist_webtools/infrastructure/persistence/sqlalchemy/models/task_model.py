from sqlalchemy import Column, Date, Enum, String, Index

from src.shared.infrastructure.persistence.sqlalchemy.engine import Base
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus


class TaskModel(Base):
    __tablename__ = "nutritionist_tasks"

    id = Column(String(50), primary_key=True)
    nutritionist_id = Column(String(50), index=True, nullable=False)
    task_name = Column(String(255), nullable=False)
    task_description = Column(String, nullable=True)
    status = Column(String(20), nullable=False, default=TaskStatus.BACKLOG.value)
    deadline_date = Column(Date, nullable=False)


Index("idx_nutritionist_tasks_nutritionist_id", TaskModel.nutritionist_id)
