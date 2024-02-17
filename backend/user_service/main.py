from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://admin:password123@localhost:27017/")
db = client["user_data"]  # Troque "your_database" pelo nome do seu banco de dados
collection = db["beneficiary"]

# Definição do modelo de dados
class BeneficiaryCreate(BaseModel):
    fullname: str
    email: str
    documentNumber: str
    phone: int
    beneficiary_type: str  # 'person' or 'institution'

# Instância do aplicativo FastAPI
app = FastAPI()

# Endpoint para criar beneficiários
@app.post("/beneficiaries/")
async def create_beneficiary(beneficiary: BeneficiaryCreate):
    # Verificar se o tipo de beneficiário é válido
    if beneficiary.type not in ['person', 'institution']:
        raise HTTPException(status_code=400, detail="Invalid beneficiary type")

    # Inserir o beneficiário no banco de dados MongoDB
    result = collection.insert_one(beneficiary.dict())

    # Verificar se a inserção foi bem-sucedida
    if result.inserted_id:
        return {"message": "Beneficiary created successfully", "beneficiary_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create beneficiary")
