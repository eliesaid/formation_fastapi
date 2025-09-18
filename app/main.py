# seed admin + seed catalogue + middleware + include_routers

from fastapi import FastAPI
from .core.database import Base, engine, SessionLocal
from .core.security import hash_password
from .models.models import User, Product
from .api.middleware import logging_middleware
from .api.routers import root, products, users, auth, cart

# Création des tables
Base.metadata.create_all(bind=engine)

# App
app = FastAPI(title="E-commerce API – Final (modulaire + background + middleware)")

# Middleware global (logs + temps d'exécution)
app.middleware("http")(logging_middleware)

# Seed au démarrage : admin + catalogue si vide
@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        # Admin
        if not db.query(User).filter(User.is_admin == True).first():  # noqa: E712
            admin = User(email="admin@example.com", password_hash=hash_password("admin"), is_admin=True)
            db.add(admin)
            db.commit()

        # Catalogue
        if db.query(Product).count() == 0:
            seed_products = [
                Product(name="T-Shirt",    description="Coton bio",           price_cents=1999),
                Product(name="Mug",        description="Céramique blanche",   price_cents=1299),
                Product(name="Casquette",  description="Style urbain",        price_cents=1599),
                Product(name="Sac à dos",  description="Polyester 20L",       price_cents=3499),
            ]
            db.add_all(seed_products)
            db.commit()
            print("✅ Catalogue initial inséré (4 produits).")
    finally:
        db.close()

# Routers
app.include_router(root.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(cart.router)
