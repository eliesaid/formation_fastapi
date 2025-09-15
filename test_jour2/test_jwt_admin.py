from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI(title="API Admin sécurisée")

# 🔐 Config JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔐 Sécurité mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 OAuth2 pour Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 🧠 Base simulée
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("adminpass"),
        "role": "admin"
    }
}

# 📦 Modèles
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class NewAdmin(BaseModel):
    username: str
    password: str

# 🔧 Fonctions utilitaires
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(username: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None or username not in users_db:
            raise HTTPException(status_code=401, detail="Jeton invalide")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Jeton expiré ou corrompu")

def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé à l'admin")
    return user

# 🚀 Routes

@app.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token(user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users")
def list_users(admin: dict = Depends(require_admin)):
    return {"users": list(users_db.keys())}

@app.post("/add-admin")
def add_admin(new_admin: NewAdmin, admin: dict = Depends(require_admin)):
    if new_admin.username in users_db:
        raise HTTPException(status_code=400, detail="Admin déjà existant")
    users_db[new_admin.username] = {
        "username": new_admin.username,
        "hashed_password": pwd_context.hash(new_admin.password),
        "role": "admin"
    }
    return {"message": f"Nouvel admin '{new_admin.username}' ajouté ✅"}
