from datetime import date
from typing import List

from src.nutritionist_webtools.domain.model.aggregates.task import Task
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus
from src.nutritionist_webtools.domain.repositories.task_repository import TaskRepository


class TaskCommandService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def _normalize_status(self, status: TaskStatus | str) -> TaskStatus:
        if isinstance(status, TaskStatus):
            return status
        return TaskStatus.from_string(status)

    def create_task(
        self,
        *,
        nutritionist_id: str,
        task_name: str,
        task_description: str | None,
        status: TaskStatus | str,
        deadline_date: date,
    ) -> Task:
        normalized_status = self._normalize_status(status)
        task = Task.create(
            nutritionist_id=nutritionist_id,
            task_name=task_name,
            task_description=task_description,
            status=normalized_status,
            deadline_date=deadline_date,
        )
        self.task_repository.save(task)
        return task

    def list_tasks(self, *, nutritionist_id: str) -> List[Task]:
        return self.task_repository.list_by_nutritionist(nutritionist_id)

    def delete_task(self, *, task_id: str) -> None:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        self.task_repository.delete(task)

    def move_task(self, *, task_id: str, status: TaskStatus | str) -> Task:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        normalized_status = self._normalize_status(status)
        task.move_to(normalized_status)
        self.task_repository.save(task)
        return task
