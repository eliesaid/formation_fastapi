from fastapi import FastAPI, Request

app = FastAPI()

# 🧱 Middleware HTTP : logue chaque requête et ajoute un header de version
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 🔍 Log de la méthode et de l'URL
    print(f"➡️ Méthode : {request.method} | URL : {request.url}")

    # 🔄 Appel de la route
    response = await call_next(request)

    # 🏷️ Ajout d’un header personnalisé
    response.headers["X-App-Version"] = "1.0"

    return response

# 📡 Route de test pour illustrer le middleware
@app.get("/demo")
async def demo():
    return {"message": "Middleware actif"}
