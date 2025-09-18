# utils.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"message": "Bonjour depuis utils.py 👋"}
