# database.py

from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://admin:adminpassword@mongodb:27017/")
db = client['doaquimaninho']
collection = db["users"]
