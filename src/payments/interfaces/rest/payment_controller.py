from fastapi import APIRouter, HTTPException
from src.payments.application.services.create_payment_service import CreatePaymentService
from src.payments.infrastructure.external.culqi_api_service import CulqiAPIService
from src.payments.domain.aggregates.payment import Payment

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

@router.post("/charge")
def create_payment(request: dict):
    """
    Crea un cargo único usando Culqi.
    Espera:
    {
        "amount": 50.00,
        "currency": "PEN",
        "email": "cliente@correo.com",
        "source_id": "tkn_test_4zZQF6VfrKuYHU",
        "description": "Compra de membresía VIP"
    }
    """
    try:
        payment = Payment(
            amount=request["amount"],
            currency=request["currency"],
            email=request["email"],
            source_id=request["source_id"],
            description=request["description"]
        )

        service = CreatePaymentService(CulqiAPIService())
        result = service.execute(payment)

        return {
            "message": "Pago procesado correctamente",
            "culqi_response": result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
