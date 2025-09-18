# main_j2.py — Jour 2 : rôles + JWT + panier + seed admin + seed catalogue
# -----------------------------------------------------------------------------
# 🎯 Objectifs pédagogiques
# - Authentification JWT (OAuth2 password flow)
# - Rôles (admin / user) & protections de routes
# - Panier par utilisateur authentifié
# - Seed automatique :
#    • d’un admin (admin@example.com / admin) — mot de passe HASHÉ
#    • d’un catalogue de produits en base (table products) si vide
#
# 🔒 Droits d'accès
# - Admin : accès à TOUTES les routes protégées + création produit + liste users
# - User  : accès catalogue (public) + SON panier ; pas de création produit ni liste users
#
# 🧭 Parcours utilisateur
# 1) POST /users   -> inscription libre
# 2) POST /token   -> reçoit un JWT
# 3) GET  /products -> public
# 4) POST /cart    -> JWT requis (ajout au panier)
# 5) GET  /cart    -> JWT requis (consulter son panier)
# 6) Persistance des users dans une table users
# 7)persistance des produits dans une products
# 8) persistance du panier dans une table cart_items


from typing import List, Optional
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError

from sqlalchemy import (
    create_engine, String, Integer, Boolean, ForeignKey, DateTime, func
)

# ForeignKey → relation entre tables (ex : cart_items.user_id -> users.id).
# func → fonctions SQL (ex : func.now() pour created_at).

from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session
)
# Mapped, mapped_column → typage moderne SQLAlchemy 2.0 pour les colonnes.
# relationship → lier deux tables (User <-> CartItem).
# sessionmaker → fabrique des sessions DB (SessionLocal).

# -----------------------------------------------------------------------------
# ⚙️ Config minimale (en J3 on passera par pydantic-settings)
# -----------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./app.db"
JWT_SECRET = "CHANGER_CE_SECRET_EN_PRODUCTION"   # ⚠️ à changer en prod
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# -----------------------------------------------------------------------------
# 🗄️ SQLAlchemy : engine + session + Base
# -----------------------------------------------------------------------------
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# -----------------------------------------------------------------------------
# 🧱 Modèles ORM
# -----------------------------------------------------------------------------
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String(255), default="")
    price_cents: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    user = relationship("User")
    product = relationship("Product")

# Crée les tables (en prod : migrations Alembic)
Base.metadata.create_all(bind=engine)

# -----------------------------------------------------------------------------
# 🔄 Dépendances FastAPI
# -----------------------------------------------------------------------------
def get_db():
    """Ouvre une session DB par requête, puis la ferme automatiquement."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # Swagger sait appeler /token

def hash_password(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    """Crée un JWT signé, avec expiration (exp)."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Extrait le user courant depuis le JWT. 401 si invalide/expiré."""
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """Vérifie le rôle admin. 403 si l'utilisateur n'est pas admin."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administrateur")
    return user

# -----------------------------------------------------------------------------
# 🧪 Schémas Pydantic (validation I/O)
# -----------------------------------------------------------------------------
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field("", max_length=255)
    price_cents: int = Field(ge=0, description="Prix en centimes (évite les flottants)")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        from_attributes = True
        # Config.from_attributes = True = autorise Pydantic à convertir 
        # un objet ORM en schéma Pydantic automatiquement.

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CartItemRead(BaseModel):
    product_id: int
    quantity: int

class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=99)

# -----------------------------------------------------------------------------
# 🚀 Application + seed admin + seed catalogue
# -----------------------------------------------------------------------------
app = FastAPI(title="E-commerce API – J2 (JWT + rôles + panier + seed catalogue)")

@app.on_event("startup")
def seed_on_startup():
    """
    👉 Au démarrage :
       1) Crée un admin 'admin@example.com' / 'admin' s'il n'existe pas (mot de passe hashé).
       2) Précharge un catalogue de produits en base si la table 'products' est vide.
    """
    db = SessionLocal()
    try:
        # 1) Seed admin (si aucun admin)
        already_admin = db.query(User).filter(User.is_admin == True).first()  # noqa: E712
        if not already_admin:
            admin = User(
                email="admin@example.com",
                password_hash=hash_password("admin"),
                is_admin=True,
            )
            db.add(admin)
            db.commit()

        # 2) Seed catalogue (si la table 'products' est vide)
        products_count = db.query(Product).count()
        if products_count == 0:
            seed_products = [
                Product(name="T-Shirt",    description="Coton bio",           price_cents=1999),
                Product(name="Mug",        description="Céramique blanche",   price_cents=1299),
                Product(name="Casquette",  description="Style urbain",        price_cents=1599),
                Product(name="Sac à dos",  description="Polyester 20L",       price_cents=3499),
            ]
            db.add_all(seed_products)
            db.commit()
            # (Optionnel) refresh si tu veux afficher les IDs en logs
            # for p in seed_products: db.refresh(p)
            print("✅ Catalogue initial inséré (4 produits).")
    finally:
        db.close()

# -----------------------------------------------------------------------------
# 🧩 Routes publiques (J1)
# -----------------------------------------------------------------------------
@app.get("/", tags=["root"])
def root():
    return {"message": "Bienvenue sur l'API e-commerce FastAPI 🚀"}

@app.get("/products", response_model=List[ProductRead], tags=["products"])
def list_products(db: Session = Depends(get_db)):
    """Catalogue public."""
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=ProductRead, tags=["products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Détail d'un produit. 404 si l'ID n'existe pas."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@app.get("/search", response_model=List[ProductRead], tags=["products"])
def search_products(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Recherche simple par nom (LIKE)."""
    return db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()

# -----------------------------------------------------------------------------
# 👥 Utilisateurs : inscription (libre), listing (admin)
# -----------------------------------------------------------------------------
@app.post("/users", response_model=UserRead, status_code=201, tags=["users"])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Inscription libre (non admin). Mot de passe stocké HASHÉ."""
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    u = User(email=payload.email, password_hash=hash_password(payload.password), is_admin=False)
    db.add(u); db.commit(); db.refresh(u)
    return u

@app.get("/users", response_model=List[UserRead], tags=["users"])
def list_users(_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """🔒 Admin seulement : lister tous les utilisateurs."""
    return db.query(User).all()

# -----------------------------------------------------------------------------
# 🔐 Authentification : POST /token (OAuth2 password) -> JWT
# -----------------------------------------------------------------------------
@app.post("/token", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authentifie admin ET user :
    - form_data.username = email
    - form_data.password = mot de passe en clair
    -> si OK, renvoie un JWT contenant sub = user.id
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)

# -----------------------------------------------------------------------------
# 🛒 Panier (auth requis) : POST /cart (ajout), GET /cart (lecture)
# -----------------------------------------------------------------------------
@app.post("/cart", tags=["cart"], status_code=201)
def add_to_cart(
    payload: CartAdd,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Ajoute un article au panier de l'utilisateur courant (JWT requis)."""
    product = db.get(Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit inexistant")

    # Si l'article est déjà présent -> on incrémente
    item = (db.query(CartItem)
              .filter(CartItem.user_id == user.id, CartItem.product_id == payload.product_id)
              .first())
    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(user_id=user.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)

    db.commit(); db.refresh(item)
    return {"message": "Ajouté au panier", "product_id": item.product_id, "quantity": item.quantity}

@app.get("/cart", response_model=List[CartItemRead], tags=["cart"])
def my_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retourne le panier de l'utilisateur courant (JWT requis)."""
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return [CartItemRead(product_id=i.product_id, quantity=i.quantity) for i in items]

# -----------------------------------------------------------------------------
# 🛠️ Produits : création réservée à l'admin
# -----------------------------------------------------------------------------
@app.post("/products", response_model=ProductRead, status_code=201, tags=["products"])
def create_product(
    payload: ProductCreate,
    _admin: User = Depends(get_current_admin),   # <-- exige un JWT d'admin
    db: Session = Depends(get_db)
):
    """🔒 Admin seulement : créer un produit dans le catalogue."""
    product = Product(**payload.model_dump())
    db.add(product); db.commit(); db.refresh(product)
    return product
