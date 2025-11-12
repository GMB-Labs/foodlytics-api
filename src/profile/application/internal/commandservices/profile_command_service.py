from src.profile.domain.model.aggregates.profile import Profile
from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
from src.profile.domain.model.commands.update_profile_command import UpdateProfileCommand
from src.profile.domain.model.commands.update_profile_picture_command import UpdateProfilePictureCommand
from src.profile.domain.repositories.profile_repository import ProfileRepository


class ProfileCommandService:
    def __init__(self, profile_repository: ProfileRepository):
        self.profile_repository = profile_repository

    def create_profile(self, command: CreateProfileCommand) -> Profile:
        profile = Profile.from_command(command)
        self.profile_repository.save(profile)
        return profile

    def update_profile(self, command: UpdateProfileCommand) -> Profile:
        profile = self.profile_repository.find_by_user_id(command.user_id)
        if not profile:
            raise ValueError("Profile not found.")
        profile.apply_update(command)
        self.profile_repository.save(profile)
        return profile

    def update_profile_picture(self, command: UpdateProfilePictureCommand) -> Profile:
        profile = self.profile_repository.find_by_id(command.profile_id)
        if not profile:
            raise ValueError("Profile not found.")
        profile.set_profile_picture(command.picture_data, command.picture_mime_type)
        self.profile_repository.save(profile)
        return profile

    def delete_profile(self, user_id: str) -> None:
        profile = self.profile_repository.find_by_user_id(user_id)
        if not profile:
            raise ValueError("Profile not found.")
        self.profile_repository.delete(profile)
