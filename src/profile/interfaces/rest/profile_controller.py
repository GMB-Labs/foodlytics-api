from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
class ProfileController():

    router = APIRouter(prefix="/profile", tags=["Profile"])
    def hola_causas(self):
        return {"message": "Hola causas!"}