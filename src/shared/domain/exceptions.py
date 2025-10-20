class DomainError(Exception):
    pass

class NotFoundError(DomainError):
    def __init__(self, entity: str):
        super().__init__(f"{entity} no encontrado")

class ValidationError(DomainError):
    def __init__(self, field: str, msg: str):
        super().__init__(f"Error en campo '{field}': {msg}")
