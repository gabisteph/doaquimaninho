from pydantic import BaseModel
from fastapi import UploadFile

class ProductCreate(BaseModel):
    name: str
    description: str
    validity_str: str
    image: UploadFile
    price: float
    status_sale: bool
