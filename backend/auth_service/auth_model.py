from pydantic import BaseModel

class loginCreate(BaseModel):
    email: str
    password: str