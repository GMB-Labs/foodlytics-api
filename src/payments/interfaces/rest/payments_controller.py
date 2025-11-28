import logging
import re
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.payments.culqi_service import CulqiService

router = APIRouter(prefix="/payments", tags=["Payments"])


class OrderRequest(BaseModel):
    amount: int
    currency_code: str
    description: str
    order_number: str
    expiration_date: str
    client_details: Dict[str, Any]
    confirm: bool = False
    metadata: Optional[Dict[str, Any]] = None


class WebhookEvent(BaseModel):
    type: str
    data: Dict[str, Any] = {}


def _validate_currency_code(code: str) -> str:
    normalized = (code or "").upper()
    if not re.fullmatch(r"[A-Z]{3}", normalized):
        raise HTTPException(status_code=400, detail="currency_code must be ISO 4217 alpha-3 (e.g., PEN, USD)")
    return normalized


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
    # Explicitly send confirm flag; defaults to False
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
