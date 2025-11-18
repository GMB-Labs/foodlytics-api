from datetime import datetime, timezone
from typing import Optional

from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
from src.profile.domain.model.commands.update_profile_command import UpdateProfileCommand
from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.profile_picture import ProfilePicture
from src.profile.domain.model.value_objects.activity_level import ActivityLevel
from src.shared.domain.model.aggregates.auditable_aggregate_root import AuditableAbstractAggregateRoot


class Profile(AuditableAbstractAggregateRoot):
    id: str
    user_id: str
    nutritionist_id: Optional[str]
    first_name: str
    last_name: str
    age: int
    height_cm: float
    weight_kg: float
    gender: Gender
    goal_type: GoalType
    activity_level: ActivityLevel | None
    desired_weight_kg: float | None

    def __init__(
        self,
        *,
        user_id: str,
        nutritionist_id: Optional[str],
        first_name: str,
        last_name: str,
        age: int,
        height_cm: float,
        weight_kg: float,
        gender: Gender,
        goal_type: GoalType,
        activity_level: ActivityLevel | None = None,
        desired_weight_kg: float | None = None,
        profile_picture: Optional[ProfilePicture] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        super().__init__(aggregate_id=user_id)
        self.id = user_id
        self.user_id = user_id
        self.nutritionist_id = nutritionist_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.gender = gender
        self.goal_type = goal_type
        self.activity_level = activity_level
        self.desired_weight_kg = desired_weight_kg
        self._profile_picture: Optional[ProfilePicture] = profile_picture

        if created_at:
            self.created_at = created_at
        if updated_at:
            self.updated_at = updated_at

    @classmethod
    def from_command(cls, command: CreateProfileCommand) -> "Profile":
        return cls(
            user_id=command.user_id,
            nutritionist_id=command.nutritionist_id,
            first_name=command.first_name,
            last_name=command.last_name,
            age=command.age,
            height_cm=command.height_cm,
            weight_kg=command.weight_kg,
            gender=command.gender,
            goal_type=command.goal_type,
            activity_level=command.activity_level,
            desired_weight_kg=command.desired_weight_kg,
        )

    def apply_update(self, command: UpdateProfileCommand) -> None:
        if command.first_name is not None:
            self.first_name = command.first_name
        if command.last_name is not None:
            self.last_name = command.last_name
        if command.age is not None:
            self.age = command.age
        if command.height_cm is not None:
            self.height_cm = command.height_cm
        if command.weight_kg is not None:
            self.weight_kg = command.weight_kg
        if command.gender is not None:
            self.gender = command.gender
        if command.goal_type is not None:
            self.goal_type = command.goal_type
        if command.activity_level is not None:
            self.activity_level = command.activity_level
        if command.desired_weight_kg is not None:
            self.desired_weight_kg = command.desired_weight_kg
        self._touch()

    def set_profile_picture(self, picture_data: bytes, mime_type: str) -> None:
        self._profile_picture = ProfilePicture(image_data=picture_data, mime_type=mime_type)
        self._touch()

    @property
    def profile_picture(self) -> Optional[ProfilePicture]:
        return self._profile_picture

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
