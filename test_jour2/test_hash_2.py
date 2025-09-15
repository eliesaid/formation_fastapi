from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI(title="Auth API - J1")

# 🔐 Sécurité : hachage avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 📦 Modèles
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

# 🧠 Stockage en mémoire
fake_users_db = {}  # username -> hashed_password

# 🚀 Routes
@app.post("/register", response_model=UserOut)
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    hashed = get_password_hash(user.password)
    fake_users_db[user.username] = hashed
    return {"username": user.username}

@app.post("/login", response_model=UserOut)
def login(user: UserLogin):
    hashed = fake_users_db.get(user.username)
    if not hashed or not verify_password(user.password, hashed):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    return {"username": user.username}
