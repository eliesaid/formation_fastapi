from fastapi import FastAPI, Request
import time

app = FastAPI()

# 🧱 Middleware HTTP : intercepte toutes les requêtes
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    # 🔍 AVANT la route : log de la requête
    print("➡️ Requête reçue :", request.method, request.url)

    start_time = time.time()  # début du chronomètre

    # 🔄 Appel de la route (ou du middleware suivant)
    response = await call_next(request)

    # ⏳ APRÈS la route : log de la réponse
    duration = time.time() - start_time
    print(f"⬅️ Réponse envoyée : {response.status_code} en {duration:.2f}s")

    # 🏷️ Ajout d’un header personnalisé (optionnel)
    response.headers["X-Process-Time"] = str(duration)

    return response

# 📡 Exemple de route pour tester le middleware
@app.get("/test")
async def test_route():
    return {"message": "Middleware en action"}
