from fastapi import APIRouter

router = APIRouter(tags=["root"])

@router.get("/")
def root():
    return {"message": "Bienvenue sur l'API e-commerce FastAPI 🚀"}
