from enum import Enum


class TaskStatus(Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"

    @classmethod
    def from_string(cls, value: str) -> "TaskStatus":
        normalized = (value or "").lower()
        for status in cls:
            if status.value == normalized:
                return status
        raise ValueError(f"Invalid task status: {value}")
