# main.py

from fastapi import FastAPI, HTTPException
from database import collection

app = FastAPI()

# Endpoint de login
@app.post("/login/")
async def login(email: str, password: str):
    # Verificar se o usuário existe no banco de dados
    user = collection.find_one({"email": email, "password": password})
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
