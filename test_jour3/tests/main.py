from fastapi import FastAPI

app = FastAPI()

# 📡 Route /info pour exposer la version de l'application
@app.get("/info")
def get_info():
    return {
        "app": "FastAPI Middleware Demo",
        "version": "1.0"
    }

