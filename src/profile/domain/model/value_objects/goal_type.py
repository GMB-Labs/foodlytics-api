from enum import Enum


class GoalType(Enum):
    DEFINITION = "definition"
    MAINTENANCE = "maintenance"
    BULKING = "bulking"

    @classmethod
    def from_string(cls, value: str) -> "GoalType":
        if not value:
            raise ValueError("Goal type cannot be empty.")
        normalized = value.strip().lower()
        for goal in cls:
            if goal.value == normalized:
                return goal
        raise ValueError(f"'{value}' is not a supported goal type.")
