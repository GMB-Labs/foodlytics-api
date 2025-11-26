import os
from typing import Any, Dict, Optional

import requests
from culqi.client import Culqi
from culqi.resources import Card, Customer, Subscription
from src.shared.infrastructure.settings import settings


class CulqiService:
    """
    Wrapper around Culqi Python SDK focused on subscriptions and orders flow.
    """

    def __init__(self, private_key: Optional[str] = None, public_key: Optional[str] = None) -> None:
        priv_key = private_key or settings.culqi_private_key or os.getenv("CULQI_PRIVATE_KEY")
        pub_key = public_key or settings.culqi_public_key or os.getenv("CULQI_PUBLIC_KEY") or ""
        if not priv_key:
            raise ValueError("Culqi private key is required (settings.culqi_private_key or CULQI_PRIVATE_KEY env).")

        culqi_client = Culqi(pub_key, priv_key)
        self.customer_resource = Customer(culqi_client)
        self.card_resource = Card(culqi_client)
        self.subscription_resource = Subscription(culqi_client)
        self.base_url = os.getenv("CULQI_API_URL", "https://api.culqi.com/v2")
        self.private_key = priv_key

    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a Culqi customer.
        Expected keys include: email, first_name, last_name, phone_number, address, address_city, country_code, metadata.
        """
        return self.customer_resource.create(data)

    def create_card(self, customer_id: str, token: str) -> Dict[str, Any]:
        """
        Creates a card associated to a customer using a token generated from Culqi.js.
        """
        payload = {"customer_id": customer_id, "token_id": token}
        return self.card_resource.create(payload)

    def create_subscription(self, card_id: str, plan_id: str) -> Dict[str, Any]:
        """
        Creates a subscription tying a card to a plan.
        """
        payload = {"card_id": card_id, "plan_id": plan_id}
        return self.subscription_resource.create(payload)

    def create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an order via Culqi REST API (v2/orders). Uses requests because the SDK may not expose orders.
        """
        url = f"{self.base_url}/orders"
        headers = {
            "Authorization": f"Bearer {self.private_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code not in (200, 201):
            try:
                message = response.json()
            except Exception:  # pragma: no cover - fallback if response not JSON
                message = response.text
            raise ValueError(f"Culqi order error {response.status_code}: {message}")
        return response.json()
