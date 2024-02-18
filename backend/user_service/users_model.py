from pydantic import BaseModel
from typing import Optional

class BeneficiaryCreate(BaseModel):
    user_type: str = "beneficary"
    fullname: str
    email: str
    documentNumber: str
    phone: int
    beneficiaryType: str  # 'person' or 'institution'
    password: str

class Address(BaseModel):
    street: str
    number: str
    district: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None


class RestaurantData(BaseModel):
    name: str
    phone: str
    cnpj: str
    delivers: bool
    address: Address

class DonorCreate(BaseModel):
    user_type: str = "donor"
    fullname: str
    cpf_cnpj: str
    contact_phone: str
    email: str
    password: str
    restaurant_data: RestaurantData
