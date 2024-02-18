from pydantic import BaseModel
from typing import Optional

class BeneficiaryCreate(BaseModel):
    user_type: str = "beneficary"
    fullname: str
    email: str
    documentNumber: str
    phone: int
    beneficiaryType: str  # 'person' or 'institution'

class Address(BaseModel):
    street: str
    number: str
    district: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None

class LegalRepresentative(BaseModel):
    fullname: str
    date_of_birth: str
    cpf_cnpj: str
    contact_phone: str
    email: str
    password: str

class RestaurantData(BaseModel):
    name: str
    phone: str
    cnpj: str
    delivers: bool
    address: Address
    legal_representative: LegalRepresentative

class DonorCreate(BaseModel):
    user_type: str = "donor"
    restaurant_data: RestaurantData
