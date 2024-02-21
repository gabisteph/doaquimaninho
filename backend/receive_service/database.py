from pymongo import MongoClient

# Conexão com o banco de dados MongoDB
client = MongoClient('mongodb://admin:adminpassword@mongodb:27017/')

db = client['doaquimaninho']

collection = db['shoppingCarts']
collection_users = db['users']
collection_products = db['product']