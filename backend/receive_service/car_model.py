from typing import List, Optional
from pydantic import BaseModel

class ProductInCart(BaseModel):
    product_id: str

class ShoppingCart(BaseModel):
    user_id: str
    products: List[ProductInCart]

class ShoppingCartCreate(BaseModel):
    user_id: str

class ShoppingCartUpdate(BaseModel):
    products: List[ProductInCart]

class ShoppingCartResponse(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    products: Optional[List[ProductInCart]] = []


class delivery_status(BaseModel):
    delivery_status: str # 'delivered', 'canceled' , 'in progress' or 'finished'
class ShoppingCartDeliveryResponse(BaseModel):
    ShoppingCart = ShoppingCartResponse
    delivery_status = delivery_status

class shoppingCartAvailable(BaseModel):
    cart = ShoppingCartDeliveryResponse
    rating: int
    description: Optional[str]
class ShoppingCartDB(ShoppingCartResponse):
    class Config:
        orm_mode = True