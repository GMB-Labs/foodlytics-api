from fastapi import APIRouter
from pydantic import BaseModel
from src.subscriptions.application.create_charge_service import CreateChargeService

router = APIRouter(prefix="/payments", tags=["Payments"])

class ChargeRequest(BaseModel):
    token_id: str
    amount: int
    email: str

@router.post("/charge")
def create_charge(data: ChargeRequest):
    service = CreateChargeService()
    return service.execute(
        token_id=data.token_id,
        amount=data.amount,
        email=data.email
    )
