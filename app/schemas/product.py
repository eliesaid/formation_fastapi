from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: str = ""
    price_cents: int = Field(ge=0, description="Prix en centimes")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        from_attributes = True
