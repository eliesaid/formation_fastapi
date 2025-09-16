from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI(title="API Produits avec SQLAlchemy")

# 🔗 Connexion SQLite
DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# 🧱 Modèle SQLAlchemy
class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

# 📦 Schémas Pydantic
class ProductCreate(BaseModel):
    name: str
    price: float

class ProductRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True

# 🛠 Initialisation de la base
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# 🔧 Dépendance session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 Endpoints

@app.post("/products", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductDB(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()
