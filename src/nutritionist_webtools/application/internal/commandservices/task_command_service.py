from datetime import date
from typing import List

from src.nutritionist_webtools.domain.model.aggregates.task import Task
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus
from src.nutritionist_webtools.domain.repositories.task_repository import TaskRepository


class TaskCommandService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(
        self,
        *,
        nutritionist_id: str,
        task_name: str,
        task_description: str | None,
        status: TaskStatus,
        deadline_date: date,
    ) -> Task:
        task = Task.create(
            nutritionist_id=nutritionist_id,
            task_name=task_name,
            task_description=task_description,
            status=status,
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

    def move_task(self, *, task_id: str, status: TaskStatus) -> Task:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        task.move_to(status)
        self.task_repository.save(task)
        return task
