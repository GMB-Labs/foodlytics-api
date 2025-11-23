from fastapi import APIRouter, Request, HTTPException
from src.subscriptions.application.webhook_handler_service import WebhookHandlerService

router = APIRouter(prefix="/payments/webhook", tags=["Payments Webhook"])


@router.post("")
async def handle_webhook(request: Request):
    payload = await request.json()

    if "type" not in payload:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    service = WebhookHandlerService()
    service.process(payload)

    return {"received": True}
