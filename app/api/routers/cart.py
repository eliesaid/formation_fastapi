from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.models import CartItem, Product
from ...schemas.cart import CartAdd, CartItemRead

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("", status_code=status.HTTP_201_CREATED)
def add_to_cart(payload: CartAdd, user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.get(Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit inexistant")
    item = db.query(CartItem).filter(CartItem.user_id == user.id, CartItem.product_id == payload.product_id).first()
    if item: item.quantity += payload.quantity
    else:
        item = CartItem(user_id=user.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)
    db.commit(); db.refresh(item)
    return {"message": "Ajouté au panier", "product_id": item.product_id, "quantity": item.quantity}

@router.get("", response_model=List[CartItemRead])
def my_cart(user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return [CartItemRead(product_id=i.product_id, quantity=i.quantity) for i in items]
