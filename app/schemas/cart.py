from pydantic import BaseModel, Field

class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=99)

class CartItemRead(BaseModel):
    product_id: int
    quantity: int
