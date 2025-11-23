import requests
from src.shared.infrastructure.settings import settings


class CulqiClient:
    BASE_URL = "https://api.culqi.com/v2"

    def __init__(self, secret_key: str | None = None):
        self.secret_key = secret_key or settings.culqi_private_key
        if not self.secret_key:
            raise ValueError("Configura CULQI_PRIVATE_KEY/culqi_private_key en .env")
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    def create_charge(self, token_id: str, amount: int, email: str):
        payload = {
            "amount": amount,
            "currency_code": "PEN",
            "email": email,
            "source_id": token_id,
        }
        response = requests.post(
            f"{self.BASE_URL}/charges",
            headers=self.headers,
            json=payload,
        )
        return response.json()
