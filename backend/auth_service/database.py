from pymongo import MongoClient
from auth_model import User

# Configurações do MongoDB
MONGO_URI = "mongodb://admin:adminpassword@mongodb:27017/"
DB_NAME = "user_data"
COLLECTION_NAME = "users"

def authenticate_user(user: User):
    try:
        # Inicialize o cliente MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Consulta o usuário no banco MongoDB usando os dados recebidos
        user_data = collection.find_one({"email": user.email, "password": user.password})

        if user_data:
            # Retorna os dados do usuário se ele existir
            print("Dados do usuário encontrados:", user_data)
            return user_data
        else:
            print("Usuário não encontrado.")
            return None
    except Exception as e:
        print(f"Erro ao autenticar o usuário: {e}")
        return None
    finally:
        client.close()
