from typing import Optional

from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.profile_picture import ProfilePicture
from src.shared.domain.model.aggregates.auditable_aggregate_root import AuditableAbstractAggregateRoot


class Profile(AuditableAbstractAggregateRoot):
    id: str
    user_id: str
    nutritionist_id: str
    first_name: str
    last_name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: Gender
    goal_type: GoalType
    profile_picture: ProfilePicture

    def __init__(self,command: CreateProfileCommand):
        super().__init__()
        self.id = command.user_id
        self.user_id = command.user_id
        self.nutritionist_id = command.nutritionist_id
        self._first_name: str = command.first_name
        self._age: int = command.age
        self._height_cm: float = command.height_cm
        self._weight_kg: float = command.weight_kg
        self._gender: Gender = command.gender
        self._goal_type: GoalType = command.goal_type

        self._profile_picture: Optional[ProfilePicture] = None

    def set_profile_picture(self,picture_data:bytes, mime_type:str):
        pass