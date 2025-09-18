from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_current_admin
from ...models.models import Product
from ...schemas.product import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return p

@router.get("/search", response_model=List[ProductRead])
def search_products(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), _admin = Depends(get_current_admin)):
    product = Product(**payload.model_dump())
    db.add(product); db.commit(); db.refresh(product)
    return product
