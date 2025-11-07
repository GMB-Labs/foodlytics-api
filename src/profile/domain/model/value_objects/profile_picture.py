from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ProfilePicture:
    """
    Value object representing a profile picture.
    """
    image_data: bytes
    mime_type: str

    def __post_init__(self):
        max_bytes = 5 * 1024 * 1024

        if not self.image_data:
            raise ValueError("Image data cannot be empty.")
        #Validates the image size and if it weights more than 5 mb, will turn into a webp file
        if len(self.image_data) > max_bytes:
            raise ValueError("Image file size exceeds the ABSOLUTE 5MB limit.")