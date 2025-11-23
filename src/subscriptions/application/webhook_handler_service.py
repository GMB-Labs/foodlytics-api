class WebhookHandlerService:

    def process(self, payload: dict):
        event_type = payload["type"]
        data = payload.get("data", {})

        if event_type == "charge.succeeded":
            charge_id = data.get("id")
            amount = data.get("amount")
            email = data.get("email")

            print("Pago aprobado:", charge_id)

            # Aquí actualizas tu base de datos a "pagado"

        elif event_type == "charge.failed":
            print("Pago fallido:", data.get("id"))

            # Aquí actualizas tu base de datos a "fallido"

        else:
            print("Evento recibido de Culqi:", event_type)
