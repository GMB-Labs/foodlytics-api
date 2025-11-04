from src.payments.domain.repositories.payment_repository import PaymentRepository


class InMemoryPaymentRepository(PaymentRepository):
    def __init__(self):
        self._payments = []

    def save(self, payment):
        self._payments.append(payment)
        return payment
