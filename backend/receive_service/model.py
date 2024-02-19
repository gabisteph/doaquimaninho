from pydantic import BaseModel
from fastapi import UploadFile

class CarStore(BaseModel):
    name: str
    price: float