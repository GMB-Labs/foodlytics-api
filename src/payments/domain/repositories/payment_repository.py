from abc import ABC, abstractmethod
from src.payments.domain.aggregates.payment import Payment


class PaymentRepository(ABC):

    @abstractmethod
    def save(self, payment: Payment):
        pass
