# main.py
from fastapi import FastAPI
from utils import router  # ✅ import du router défini dans utils.py

app = FastAPI(title="App modulaire avec utils")

# 🔗 Inclusion des routes externes
app.include_router(router, prefix="/utils", tags=["utils"])

