from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UpdateProfilePictureCommand:
    """
    Command to patch a profile picture.
    """
    profile_id: str
    picture_data: bytes
    picture_mime_type: str
