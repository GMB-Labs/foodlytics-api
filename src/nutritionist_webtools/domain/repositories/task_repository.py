from abc import ABC, abstractmethod
from typing import List, Optional

from src.nutritionist_webtools.domain.model.aggregates.task import Task
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    def list_by_nutritionist(self, nutritionist_id: str) -> List[Task]:
        ...

    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        ...

    @abstractmethod
    def save(self, task: Task) -> None:
        ...

    @abstractmethod
    def delete(self, task: Task) -> None:
        ...
