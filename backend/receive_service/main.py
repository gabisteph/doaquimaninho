from fastapi import FastAPI, HTTPException
from typing import List
from bson import ObjectId
from pymongo import MongoClient
from database import collection, collection_users, collection_products
from car_model import ShoppingCart, ShoppingCartCreate, ShoppingCartUpdate, ShoppingCartResponse, ShoppingCartDB, shoppingCartAvailable, ShoppingCartDeliveryResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Operações no banco de dados
# Aqui verifico se o usuário existe no banco de dados
def user_exists(user_id: str) -> bool:
    user = collection_users.find_one({"_id": ObjectId(user_id)})
    return user is not None
# Aqui verifico se o produto existe no banco de dados
def product_exists(product_id: str) -> bool:
    product = collection_products.find_one({"_id": ObjectId(product_id)})
    return product is not None
# Aqui eu verifico se o usuário existe e crio o carrinho
def create_cart(cart_data: ShoppingCartCreate) -> str:

    # Verifica se o user_id existe no banco de dados
    if not user_exists(cart_data.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    # foooooi, cria o carrinho de compras
    result = collection.insert_one(cart_data.dict())
    return str(result.inserted_id)
# Aqui eu pego o carrinho pelo id
def get_cart_by_id(cart_id: str) -> dict:
    cart = collection.find_one({"_id": ObjectId(cart_id)})
    if cart:
        cart['_id'] = str(cart['_id'])  # Converte ObjectId para str
    return cart
# Aqui eu atualizo o carrinho
def update_cart(cart_id: str, cart_data: ShoppingCartUpdate) -> None:
    collection.update_one({"_id": ObjectId(cart_id)}, {"$set": cart_data.dict()})
# Aqui eu deleto o carrinho
def delete_cart(cart_id: str) -> None:
    collection.delete_one({"_id": ObjectId(cart_id)})
# Ao finalizar pedido, é adiciona um status de entrega
def update_delivery(cart_id: str, cart_data: ShoppingCartUpdate, delivery_status: str) -> None:
    cart_data_dict = cart_data.dict()
    cart_data_dict["delivery_status"] = delivery_status
    collection.update_one({"_id": ObjectId(cart_id)}, {"$set": cart_data_dict})

# avalia o carrinho
def update_avaliable(cart_id: str, cart_data: shoppingCartAvailable) -> None:
    # Verifique se o carrinho de compras está disponível para atualização
    existing_cart = get_cart_by_id(cart_id)
    if existing_cart:
        # Atualize o carrinho com a classificação e o status de entrega
        update_data = {
            "rating": cart_data.rating,
            "description": cart_data.description,
            "delivery_status": cart_data.cart.delivery_status.delivery_status  # Acessando o status de entrega do modelo
        }
        # Atualize o carrinho com os novos dados
        collection.update_one({"_id": ObjectId(cart_id)}, {"$set": update_data})
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

# Rotas da API
# inicializa carrinho
@app.post("/carts/", response_model=ShoppingCartResponse)
async def create_shopping_cart(cart_data: ShoppingCartCreate):
    cart_id = create_cart(cart_data)
    return {"id": cart_id, **cart_data.dict()}
# pega carrinho pelo id
@app.get("/carts/{cart_id}", response_model=ShoppingCartResponse)
async def read_shopping_cart(cart_id: str):
    cart = get_cart_by_id(cart_id)
    if cart:
        return cart
    else:
        raise HTTPException(status_code=404, detail="Cart not found")
# adiciona produto ao carrinho
@app.put("/carts/{cart_id}", response_model=ShoppingCartResponse)
async def update_shopping_cart(cart_id: str, cart_data: ShoppingCartUpdate):
    # Verificar a existência dos produtos atualizados
    for product_in_cart in cart_data.products:
        if not product_exists(product_in_cart.product_id):
            raise HTTPException(status_code=404, detail=f"Product {product_in_cart.product_id} not found")

    # Verificar se o carrinho de compras existe
    existing_cart = get_cart_by_id(cart_id)
    if existing_cart:
        update_cart(cart_id, cart_data)
        return {"id": cart_id, **cart_data.dict()}
    else:
        raise HTTPException(status_code=404, detail="Cart not found")
# deleta carrinho
@app.delete("/carts/{cart_id}")
async def delete_shopping_cart(cart_id: str):
    existing_cart = get_cart_by_id(cart_id)
    if existing_cart:
        delete_cart(cart_id)
        return {"message": f"Cart {cart_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

# status de entrega
@app.put("/carts/delivery/{cart_id}")
async def update_shopping_cart(cart_id: str, cart_data: ShoppingCartUpdate, delivery_status: str = "in progress"):

    # Verificar a existência dos produtos atualizados
    for product_in_cart in cart_data.products:
        if not product_exists(product_in_cart.product_id):
            raise HTTPException(status_code=404, detail=f"Product {product_in_cart.product_id} not found")

    # Verificar se o carrinho de compras existe
    existing_cart = get_cart_by_id(cart_id)
    if existing_cart:
        update_delivery(cart_id, cart_data, delivery_status)
        return {"id": cart_id, **cart_data.dict(), "delivery_status": delivery_status}
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

@app.put("/carts/available/{cart_id}", response_model=ShoppingCartResponse)
async def update_shopping_cart(cart_id: str, cart_data: shoppingCartAvailable):
    # Verificar a existência dos produtos atualizados
    for product_in_cart in cart_data.products:
        if not product_exists(product_in_cart.product_id):
            raise HTTPException(status_code=404, detail=f"Product {product_in_cart.product_id} not found")

    # Verificar se o carrinho de compras existe
    existing_cart = get_cart_by_id(cart_id)
    if existing_cart:
        # Você precisa implementar a função update_avaliable()
        update_avaliable(cart_id, cart_data)
        # Considerando que delivery_status é um campo do modelo shoppingCartAvailable
        return {"id": cart_id, **cart_data.dict(), "delivery_status": cart_data.delivery_status}
    else:
        raise HTTPException(status_code=404, detail="Cart not found")
