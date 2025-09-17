from fastapi import FastAPI, Depends

app = FastAPI()

# 🔧 Dépendance de base : paramètres de configuration
def get_settings():
    # Simule un chargement de configuration (ex: depuis un fichier ou des variables d'environnement)
    return {
        "app_name": "gestion-locative",
        "db_user": "admin",
        "db_name": "locative_db"
    }

# 🔗 Sous-dépendance : construit l'URL de la base à partir des settings
def get_db_url(settings: dict = Depends(get_settings)):
    user = settings["db_user"]
    db_name = settings["db_name"]
    return f"postgresql://{user}@localhost:5432/{db_name}"

# 📡 Route principale : utilise la dépendance chaînée
@app.get("/db-url")
def show_db_url(db_url: str = Depends(get_db_url)):
    return {"db_url": db_url}

