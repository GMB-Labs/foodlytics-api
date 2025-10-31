from src.payments.infrastructure.external.culqi_api_service import CulqiAPIService
from src.payments.domain.aggregates.payment import Payment


class CreatePaymentService:
    def __init__(self, culqi_service: CulqiAPIService):
        self.culqi_service = culqi_service

    def execute(self, payment: Payment):
        response = self.culqi_service.create_charge(
            amount=payment.amount.value,
            currency_code=payment.currency,
            email=payment.email,
            source_id=payment.source_id,
            description=payment.description
        )
        return response
