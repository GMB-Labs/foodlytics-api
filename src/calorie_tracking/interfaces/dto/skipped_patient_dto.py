from pydantic import BaseModel


class SkippedPatientDTO(BaseModel):
    patient_id: str
    reason: str
