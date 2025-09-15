from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Product(BaseModel):
    name: str = Field(..., example="Chaussures de sport")
    price: float = Field(..., gt=0, example=59.99)
    in_stock: bool = True

@app.post("/products/")
def create_product(product: Product):
    return {"message": "Produit ajouté", "produit": product}
