class AmountVO:
    def __init__(self, value: float):
        if value <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        self.value = int(value * 100)  # Culqi usa centavos
