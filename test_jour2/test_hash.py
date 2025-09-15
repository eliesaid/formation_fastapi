from fastapi import FastAPI
from passlib.context import CryptContext

app = FastAPI(title="Demo Passlib")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/hash/{password}")
def hash_password(password: str):
    hashed = pwd_context.hash(password)
    return {"hashed_password": hashed}

@app.get("/verify")
def verify_password(password: str, hashed: str):
    valid = pwd_context.verify(password, hashed)
    return {"valid": valid}
