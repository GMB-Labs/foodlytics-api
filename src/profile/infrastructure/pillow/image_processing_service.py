from PIL import Image
from io import BytesIO

class ImageProcessingService:
    @staticmethod
    def convert_to_webp(image_data: bytes, original_mime_type:str) -> tuple[bytes, str]:
        if original_mime_type in ['image/webp', 'image/gif']:
            return image_data, original_mime_type
        try:
            img = Image.open(BytesIO(image_data))
            output = BytesIO()
            img.save(output, format="WEBP", optimize=True, quality=85)
            webp_data = output.getvalue()
            return webp_data, "image/webp"
        except Exception as e:
            raise ValueError("Failed to convert image to WEBP format") from e