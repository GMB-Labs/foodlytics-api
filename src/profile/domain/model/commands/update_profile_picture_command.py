from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UpdateProfilePictureCommand:
    """
    Command to patch a profile picture.
    """
    profile_id: int
    picture_data: bytes
    picture_mime_type: str