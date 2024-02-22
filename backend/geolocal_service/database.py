from pymongo import MongoClient
from auth_model import User

# Inicialize o cliente MongoDB
client = MongoClient('mongodb://admin:adminpassword@mongodb:27017/')

db = client['doaquimaninho']
users_collection = db['users']

def authenticate_user(user: User):
    user_data = users_collection.find_one({"email": user.email})
    if user_data and user_data["password"] == user.password:
        return User(**user_data)
    return None

def get_user(email: str):
    user_data = users_collection.find_one({"email": email})
    if user_data:
        return User(**user_data)
    return None
