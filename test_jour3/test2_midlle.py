from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

@app.middleware("http")
async def log_middleware(request, call_next):
    print("Requête reçue :", request.method, request.url)
    response = await call_next(request)
    print("Réponse envoyée :", response.status_code)
    return response

# 📡 Route de test pour illustrer le logging
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# 📡 Autre route pour varier les requêtes
@app.get("/info")
async def info():
    return {"app": "FastAPI Middleware Demo", "version": "1.0"}


