from pydantic import BaseModel
from typing import Optional

class BeneficiaryCreate(BaseModel):
    fullname: str
    email: str
    document_number: str
    phone: int
    beneficiary_type: str  # 'person' or 'institution'

class Address(BaseModel):
    street: str
    number: str
    district: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None

class LegalRepresentative(BaseModel):
    full_name: str
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
