from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError

app = FastAPI(title="JWT Demo")

# 🔐 Configuration JWT
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 📦 Modèles
class TokenRequest(BaseModel):
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 🔧 Fonctions JWT
def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Jeton invalide ou expiré")

# 🚀 Routes
@app.post("/token", response_model=TokenResponse)
def generate_token(data: TokenRequest):
    token = create_access_token(data.username)
    return {"access_token": token}

@app.get("/protected")
def protected_route(token: str):
    username = decode_token(token)
    return {"message": f"Bienvenue {username}, accès autorisé ✅"}

