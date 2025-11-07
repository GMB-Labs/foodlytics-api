from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
class ProfileCommandService:
    def __init__(self, profile_repository:ProfileRepository):
        self.profile_repository = profile_repository

    def create_profile(self, create_profile_command: CreateProfileCommand):
        # Logic to create a new profile
        return self.profile_repository.add(create_profile_command)

    def update_profile(self, profile_id, profile_data):
        # Logic to update an existing profile
        return self.profile_repository.update(profile_id, profile_data)

    def delete_profile(self, profile_id):
        # Logic to delete a profile
        return self.profile_repository.delete(profile_id)