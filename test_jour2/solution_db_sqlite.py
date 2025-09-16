# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# -------------------------------------------------------------------
# 1) CONFIG DB: SQLAlchemy + SQLite local
# -------------------------------------------------------------------
DATABASE_URL = "sqlite:///./app.db"  # fichier local (aucun serveur à installer)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # nécessaire pour SQLite en single-thread
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    """Dépendance FastAPI: ouvre/ferme une session SQLAlchemy par requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------------------
# 2) MODELE SQLAlchemy (table users)
# -------------------------------------------------------------------
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

# -------------------------------------------------------------------
# 3) SCHÉMAS Pydantic (validation I/O)
# -------------------------------------------------------------------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, example="alice")
    email: EmailStr = Field(..., example="alice@example.com")

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # (Pydantic v2) ; utiliser orm_mode=True en v1

# -------------------------------------------------------------------
# 4) APP + création des tables
# -------------------------------------------------------------------
app = FastAPI(title="Exercice /users - SQLite + SQLAlchemy")

Base.metadata.create_all(bind=engine)  # crée la table si absente

# -------------------------------------------------------------------
# 5) ENDPOINTS /users
# -------------------------------------------------------------------
@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Vérifier unicité username / email
    conflict = (
        db.query(UserDB)
        .filter((UserDB.username == user_in.username) | (UserDB.email == user_in.email))
        .first()
    )
    if conflict:
        raise HTTPException(status_code=400, detail="Username ou email déjà utilisé")

    user = UserDB(username=user_in.username, email=user_in.email)
    db.add(user)
    db.commit()
    db.refresh(user)  # récupère l'ID depuis la DB
    return user

@app.get("/users", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()


