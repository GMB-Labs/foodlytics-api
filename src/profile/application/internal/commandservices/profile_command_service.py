from src.profile.domain.events import ProfileUpdatedEvent
from src.profile.domain.model.aggregates.profile import Profile
from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
from src.profile.domain.model.commands.update_profile_command import UpdateProfileCommand
from src.profile.domain.model.commands.update_profile_picture_command import UpdateProfilePictureCommand
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.shared.domain.events.event_bus import EventBus


class ProfileCommandService:
    def __init__(self, profile_repository: ProfileRepository, event_bus: EventBus | None = None):
        self.profile_repository = profile_repository
        self._event_bus = event_bus

    def create_profile(self, command: CreateProfileCommand) -> Profile:
        profile = Profile.from_command(command)
        self.profile_repository.save(profile)
        self._publish_profile_updated(profile)
        return profile

    def update_profile(self, command: UpdateProfileCommand) -> Profile:
        profile = self.profile_repository.find_by_user_id(command.user_id)
        if not profile:
            raise ValueError("Profile not found.")
        profile.apply_update(command)
        self.profile_repository.save(profile)
        self._publish_profile_updated(profile)
        return profile

    def update_profile_picture(self, command: UpdateProfilePictureCommand) -> Profile:
        profile = self.profile_repository.find_by_id(command.profile_id)
        if not profile:
            raise ValueError("Profile not found.")
        profile.set_profile_picture(command.picture_data, command.picture_mime_type)
        self.profile_repository.save(profile)
        return profile

    def update_weight(self, *, user_id: str, weight_kg: float) -> Profile:
        profile = self.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found.")

        event = profile.update_weight(weight_kg=weight_kg)
        self.profile_repository.save(profile)

        # Publish to update calorie targets and weight history.
        if self._event_bus:
            self._event_bus.publish(event)

        return profile

    def delete_profile(self, user_id: str) -> None:
        profile = self.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found.")
        self.profile_repository.delete(profile)

    def _publish_profile_updated(self, profile: Profile) -> None:
        if not self._event_bus:
            return
        if profile.age <= 0 or profile.height_cm <= 0 or profile.weight_kg <= 0:
            return
        event = ProfileUpdatedEvent(
            user_id=profile.user_id,
            age=profile.age,
            height_cm=profile.height_cm,
            weight_kg=profile.weight_kg,
            gender=profile.gender,
            goal_type=profile.goal_type,
            activity_level=profile.activity_level,
            desired_weight_kg=profile.desired_weight_kg,
        )
        self._event_bus.publish(event)
