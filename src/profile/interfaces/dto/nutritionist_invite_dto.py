from pydantic import BaseModel, Field


class GenerateInviteResponseDTO(BaseModel):
    code: str = Field(..., description="Código de 6 dígitos para compartir con el paciente.")


class RedeemInviteRequestDTO(BaseModel):
    patient_id: str = Field(..., description="ID del paciente que se va a asociar.")
    code: str = Field(..., description="Código de 6 dígitos proporcionado por el nutricionista.")
