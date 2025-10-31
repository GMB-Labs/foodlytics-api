import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CulqiAPIService:
    def __init__(self):
        self.private_key = os.getenv("CULQI_PRIVATE_KEY")
        self.base_url = "https://api.culqi.com/v2"

    def create_charge(self, amount, currency_code, email, source_id, description):
        url = f"{self.base_url}/charges"
        headers = {
            "Authorization": f"Bearer {self.private_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount,
            "currency_code": currency_code,
            "email": email,
            "source_id": source_id,
            "description": description
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
