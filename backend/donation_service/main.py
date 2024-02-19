from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from datetime import datetime, date
from database import collection

app = FastAPI()

@app.post("/register/product/")
async def create_product(name: str = Form(...), 
                         description: str = Form(...), 
                         validity_str: str = Form(...),  # Recebe a data como string
                         image: UploadFile = File(...), 
                         price: float = Form(...),
                         status_sale: bool = Form(...)):
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