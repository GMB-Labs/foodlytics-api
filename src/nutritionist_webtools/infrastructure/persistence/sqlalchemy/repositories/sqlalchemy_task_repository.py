from typing import List, Optional
from sqlalchemy.orm import Session

from src.nutritionist_webtools.domain.model.aggregates.task import Task
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus
from src.nutritionist_webtools.domain.repositories.task_repository import TaskRepository
from src.nutritionist_webtools.infrastructure.persistence.sqlalchemy.models.task_model import TaskModel


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            nutritionist_id=model.nutritionist_id,
            task_name=model.task_name,
            task_description=model.task_description,
            status=TaskStatus.from_string(model.status),
            deadline_date=model.deadline_date,
        )

    def _sync_model(self, model: TaskModel, entity: Task) -> None:
        model.id = entity.id
        model.nutritionist_id = entity.nutritionist_id
        model.task_name = entity.task_name
        model.task_description = entity.task_description
        model.status = entity.status.value
        model.deadline_date = entity.deadline_date

    def list_by_nutritionist(self, nutritionist_id: str) -> List[Task]:
        rows = (
            self.db.query(TaskModel)
            .filter(TaskModel.nutritionist_id == nutritionist_id)
            .order_by(TaskModel.deadline_date)
            .all()
        )
        return [self._to_domain(row) for row in rows]

    def find_by_id(self, task_id: str) -> Optional[Task]:
        row = self.db.get(TaskModel, task_id)
        return self._to_domain(row) if row else None

    def save(self, task: Task) -> None:
        model = self.db.get(TaskModel, task.id)
        if model is None:
            model = TaskModel()
            self._sync_model(model, task)
            self.db.add(model)
        else:
            self._sync_model(model, task)
        self.db.commit()

    def delete(self, task: Task) -> None:
        model = self.db.get(TaskModel, task.id)
        if not model:
            return
        self.db.delete(model)
        self.db.commit()
