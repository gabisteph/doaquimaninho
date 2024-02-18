from pydantic import BaseModel, Optional
from typing import Optional
from passlib.context import CryptContext


# Modelo Pydantic para criar usuário
class UserCreate(BaseModel):
    email: str
    password: str
# Modelo Pydantic para representar usuário armazenado no banco de dados
class User(BaseModel):
    email: str
    hashed_password: str


class BeneficiaryCreate(BaseModel):
    user_type: str = "beneficary"
    fullname: str
    documentNumber: str
    phone: int
    beneficiaryType: str  # 'person' or 'institution'
    user: User

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
    documentNumber: str
    phone: str
    restaurant_data: RestaurantData
    user: User

# Criando um objeto CryptContext com o esquema bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Função para criar um usuário com senha criptografada
def create_user(user_create: UserCreate):
    # Criptografando a senha usando bcrypt
    hashed_password = pwd_context.hash(user_create.password)
    # Retornando o usuário com a senha criptografada
    return User(email=user_create.email, hashed_password=hashed_password)

