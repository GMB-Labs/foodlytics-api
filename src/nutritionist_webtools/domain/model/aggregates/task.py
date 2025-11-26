from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4
from typing import Optional

from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus


@dataclass(slots=True)
class Task:
    id: str
    nutritionist_id: str
    task_name: str
    task_description: Optional[str]
    status: TaskStatus
    deadline_date: date

    @classmethod
    def create(
        cls,
        *,
        nutritionist_id: str,
        task_name: str,
        task_description: Optional[str],
        status: TaskStatus,
        deadline_date: date,
    ) -> "Task":
        return cls(
            id=str(uuid4()),
            nutritionist_id=nutritionist_id,
            task_name=task_name,
            task_description=task_description,
            status=status,
            deadline_date=deadline_date,
        )

    def move_to(self, status: TaskStatus) -> None:
        self.status = status
