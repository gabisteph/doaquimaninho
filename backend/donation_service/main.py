from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from datetime import datetime, date
from database import collection
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register/product/")
async def create_product(name: str = Form(...), 
                         description: str = Form(...), 
                         validity_str: str = Form(...),  # Recebe a data como string
                         image: UploadFile = File(...), 
                         price: float = Form(...),
                         status_sale: bool = Form(...),
                         token: str = Depends(oauth2_scheme)):
    try:
        # Convertendo a string de data para o tipo datetime.date com formato europeu
        validity = datetime.strptime(validity_str, "%Y-%m-%d")

        # Ler o conteúdo do arquivo de imagem
        contents = await image.read()
        
        # Salvar os dados do produto no banco de dados
        product_dict = {
            "name": name,
            "description": description,
            "validity": validity,
            "image": contents,
            "price": price,
            "status_sale": status_sale
        }
        result = collection.insert_one(product_dict)
        
        if result.inserted_id:
            return {"message": "Product created successfully", "product_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create product.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Método GET para obter detalhes de um produto específico
@app.get("/products/{product_id}")
async def read_product(product_id: str, token: str = Depends(oauth2_scheme)):
    # Buscar o produto no MongoDB com base no product_id
    product = collection.find_one({"_id": product_id})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Como o _id é um ObjectId do MongoDB, precisamos converter para str antes de retornar
    product["_id"] = str(product["_id"])
    return product

    
# Método PUT para atualizar os detalhes de um produto existente
@app.put("/products/{product_id}")
async def update_product(product_id: str, name: str = Form(...), 
                         description: str = Form(...), 
                         validity_str: str = Form(...),  # Recebe a data como string
                         image: UploadFile = File(...), 
                         price: float = Form(...),
                         status_sale: bool = Form(...),
                         token: str = Depends(oauth2_scheme)):
    try:
        # Convertendo a string de data para o tipo datetime.date com formato europeu
        validity = datetime.strptime(validity_str, "%Y-%m-%d")

        # Ler o conteúdo do arquivo de imagem
        contents = await image.read()
        
        # Salvar os dados do produto no banco de dados
        product_dict = {
            "name": name,
            "description": description,
            "validity": validity,
            "image": contents,
            "price": price,
            "status_sale": status_sale
        }
        # Implemente a lógica para atualizar os detalhes do produto com o ID fornecido no banco de dados
        # Por enquanto, apenas retorne um exemplo de resposta
        return {"message": f"Product {product_id} updated successfully", "product_details": product_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Método DELETE para excluir um produto existente
@app.delete("/products/{product_id}")
async def delete_product(product_id: str, token: str = Depends(oauth2_scheme)):
    # Verificar se o produto existe
    product = collection.find_one({"_id": product_id})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Deletar o produto do MongoDB
    result = collection.delete_one({"_id": product_id})
    if result.deleted_count == 1:
        return {"message": f"Product {product_id} deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete product")