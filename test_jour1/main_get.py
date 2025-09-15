from fastapi import FastAPI

app = FastAPI(title="API Utilisateur")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "message": f"Utilisateur {user_id} récupéré avec succès"}
