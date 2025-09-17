from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ✅ Modèle de produit avec validation
class Product(BaseModel):
    name: str
    price: float  # Doit être un nombre, sinon FastAPI renvoie une erreur 422

# 📡 Route POST pour créer un produit
@app.post("/products/")
def create_product(product: Product):
    return {"product": product}
