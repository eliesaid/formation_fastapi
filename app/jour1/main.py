# main.py — Jour 1 : Catalogue produits (prix en float, préchargé)
# ------------------------------------------------------------------

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="E-commerce API - Jour 1")

# ---------------------- Schémas Pydantic ----------------------

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nom du produit")
    description: str = Field("", max_length=255, description="Description courte")
    price: float = Field(ge=0, description="Prix du produit en euros (€)")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

# ---------------------- Stockage en mémoire -------------------

PRODUCTS: List[ProductRead] = []
_next_id = 1

def _add_product(p: ProductCreate) -> ProductRead:
    """Ajoute un produit à la liste en lui donnant un id auto-incrémenté."""
    global _next_id
    obj = ProductRead(id=_next_id, **p.model_dump())
    PRODUCTS.append(obj)
    _next_id += 1
    return obj

# ---------- Préchargement du catalogue ----------
_catalogue_init = [
    ProductCreate(name="T-Shirt", description="Coton bio", price=19.99),
    ProductCreate(name="Mug", description="Céramique blanche", price=12.99),
    ProductCreate(name="Casquette", description="Style urbain", price=15.99),
    ProductCreate(name="Sac à dos", description="Polyester 20L", price=34.99),
]

for item in _catalogue_init:
    _add_product(item)

# --------------------------- Routes ---------------------------

@app.get("/", tags=["root"])
def root():
    return {"message": "Bienvenue sur l'API e-commerce FastAPI 🚀 (Jour 1)"}

@app.get("/products", response_model=List[ProductRead], tags=["products"])
def list_products():
    return PRODUCTS

@app.get("/products/{product_id}", response_model=ProductRead, tags=["products"])
def get_product(product_id: int):
    for p in PRODUCTS:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Produit non trouvé")

@app.get("/search", response_model=List[ProductRead], tags=["products"])
def search_products(query: str = Query(..., min_length=1, description="Mot-clé à chercher dans le nom")):
    q = query.lower()
    return [p for p in PRODUCTS if q in p.name.lower()]

@app.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED, tags=["products"])
def create_product(payload: ProductCreate):
    return _add_product(payload)
