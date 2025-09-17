from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

# 📬 Fonction exécutée en tâche de fond
def notify_admin(username: str):
    print(f"👤 Nouvel utilisateur inscrit : {username}")
    # Ici, tu pourrais envoyer un email, écrire dans un fichier, ou notifier via webhook

# 📦 Modèle de données pour l'inscription
class UserSignup(BaseModel):
    username: str

# 📡 Route POST avec tâche en arrière-plan
@app.post("/signup")
def signup(data: UserSignup, tasks: BackgroundTasks):
    tasks.add_task(notify_admin, data.username)
    return {"msg": f"Inscription en cours pour {data.username}"}

