# database.py

from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://admin:adminpassword@0.0.0.0:27017/")
db = client["user_data"]  # Troque "your_database" pelo nome do seu banco de dados
collection = db["users"]
