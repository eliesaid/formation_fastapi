from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

app = FastAPI(title="API sécurisée avec JWT")

# 🔐 Config JWT
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔐 Sécurité mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 OAuth2 scheme pour Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 🧠 Base utilisateur simulée
fake_users_db = {}  # username -> hashed_password

# 📦 Modèles
class UserRegister(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 🔧 Fonctions utilitaires
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Jeton invalide")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Jeton expiré ou corrompu")

# 🚀 Routes

@app.post("/register")
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    hashed = get_password_hash(user.password)
    fake_users_db[user.username] = hashed
    return {"message": f"Utilisateur {user.username} enregistré ✅"}

@app.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    hashed = fake_users_db.get(username)
    if not hashed or not verify_password(password, hashed):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token(username)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def read_me(username: str = Depends(get_current_user)):
    return {"username": username}

@app.get("/secure-data")
def secure_data(username: str = Depends(get_current_user)):
    return {"message": f"Accès autorisé pour {username} 🔐"}

