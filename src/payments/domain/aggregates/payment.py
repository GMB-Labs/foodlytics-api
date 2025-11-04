from src.payments.domain.value_objects.amount_vo import AmountVO


class Payment:
    def __init__(self, amount: float, currency: str, email: str, source_id: str, description: str):
        self.amount = AmountVO(amount)
        self.currency = currency
        self.email = email
        self.source_id = source_id
        self.description = description
