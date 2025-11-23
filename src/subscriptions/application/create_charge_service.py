from src.subscriptions.infrastructure.culqi.culqi_client import CulqiClient

class CreateChargeService:
    def __init__(self):
        self.client = CulqiClient()

    def execute(self, token_id: str, amount: int, email: str):
        charge = self.client.create_charge(token_id, amount, email)

        # Aquí opcionalmente puedes guardar un registro preliminar en DB

        return charge
