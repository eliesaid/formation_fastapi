from fastapi import FastAPI

app = FastAPI(title="API avec Tags")

@app.get("/", tags=["Accueil"])
def read_root():
    return {"message": "Hello World"}

@app.get("/bonjour", tags=["Salutations"])
def dire_bonjour():
    return {"message": "Bonjour depuis FastAPI"}
