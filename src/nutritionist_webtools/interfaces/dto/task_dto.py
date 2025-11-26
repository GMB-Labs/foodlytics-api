from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from src.nutritionist_webtools.domain.model.aggregates.task import Task
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus


class TaskRequestDTO(BaseModel):
    task_name: str = Field(..., example="Plan semanal")
    task_description: Optional[str] = Field(None, example="Preparar menú de la semana")
    status: TaskStatus = Field(default=TaskStatus.BACKLOG, description="backlog|in_progress|review|completed")
    deadline_date: date = Field(..., description="YYYY-MM-DD")

    class Config:
        use_enum_values = True


class TaskMoveRequestDTO(BaseModel):
    status: TaskStatus

    class Config:
        use_enum_values = True


class TaskResponseDTO(BaseModel):
    id: str
    nutritionist_id: str
    task_name: str
    task_description: Optional[str]
    status: TaskStatus
    deadline_date: date

    class Config:
        use_enum_values = True

    @classmethod
    def from_domain(cls, task: Task) -> "TaskResponseDTO":
        return cls(
            id=task.id,
            nutritionist_id=task.nutritionist_id,
            task_name=task.task_name,
            task_description=task.task_description,
            status=task.status,
            deadline_date=task.deadline_date,
        )
