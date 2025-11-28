import logging
import re
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from src.payments.culqi_service import CulqiService

router = APIRouter(prefix="/payments", tags=["Payments"])


class SubscribeRequest(BaseModel):
    token: str
    plan_id: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    address_city: Optional[str] = None
    country_code: str
    metadata: Optional[Dict[str, Any]] = None


class OrderRequest(BaseModel):
    amount: int
    currency_code: str
    description: str
    order_number: str
    expiration_date: str
    client_details: Dict[str, Any]
    confirm: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class WebhookEvent(BaseModel):
    type: str
    data: Dict[str, Any] = {}


def _validate_country_code(code: str) -> str:
    normalized = (code or "").upper()
    if not re.fullmatch(r"[A-Z]{2}", normalized):
        raise HTTPException(status_code=400, detail="country_code must be ISO-3166-1 alpha-2 (e.g., PE)")
    return normalized


def _validate_currency_code(code: str) -> str:
    normalized = (code or "").upper()
    if not re.fullmatch(r"[A-Z]{3}", normalized):
        raise HTTPException(status_code=400, detail="currency_code must be ISO 4217 alpha-3 (e.g., PEN, USD)")
    return normalized


@router.post("/subscribe")
def subscribe(request: SubscribeRequest):
    country_code = _validate_country_code(request.country_code)
    service = CulqiService()
    customer_payload = {
        "email": request.email,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "phone_number": request.phone_number,
        "address": request.address,
        "address_city": request.address_city,
        "country_code": country_code,
        "metadata": request.metadata,
    }
    try:
        customer = service.create_customer(customer_payload)
        card = service.create_card(customer_id=customer.get("id"), token=request.token)
        subscription = service.create_subscription(card_id=card.get("id"), plan_id=request.plan_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Subscription created",
        "customer_id": customer.get("id"),
        "card_id": card.get("id"),
        "subscription_id": subscription.get("id"),
    }


@router.post("/orders")
def create_order(request: OrderRequest):
    service = CulqiService()
    currency = _validate_currency_code(request.currency_code)
    payload = {
        "amount": request.amount,
        "currency_code": currency,
        "description": request.description,
        "order_number": request.order_number,
        "expiration_date": request.expiration_date,
        "client_details": request.client_details,
    }
    if request.confirm is not None:
        payload["confirm"] = request.confirm
    if request.metadata is not None:
        payload["metadata"] = request.metadata

    try:
        order_response = service.create_order(payload)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return order_response


@router.post("/orders/{order_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_order(order_id: str):
    service = CulqiService()
    try:
        return service.confirm_order(order_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/webhook")
def webhook(event: WebhookEvent):
    logging.info("Culqi webhook received: %s", event.type)
    print(f"Culqi webhook received: {event.type} -> {event.data}")
    return {"status": "received", "event": event.type}
