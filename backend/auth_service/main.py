# main.py

from fastapi import FastAPI, HTTPException
from .database import collection
from .auth_model import loginCreate

app = FastAPI()

# Endpoint de login
@app.post("/login/")
async def login(login: loginCreate):
    # Verificar se o usuário existe no banco de dados
    user = collection.find_one({"email": login.email, "password": login.password})
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
