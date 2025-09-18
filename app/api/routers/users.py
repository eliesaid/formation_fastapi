# ✅ BackgroundTasks ici

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import hash_password, get_current_admin
from ...models.models import User
from ...schemas.user import UserCreate, UserRead
from ...services.notifications import send_welcome_email

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Inscription libre :
    - persiste l'utilisateur (is_admin=False)
    - mot de passe stocké HASHÉ
    - déclenche une tâche asynchrone (BackgroundTasks) pour notifier
    """
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    u = User(email=payload.email, password_hash=hash_password(payload.password), is_admin=False)
    db.add(u); db.commit(); db.refresh(u)

    # 🔔 Background task de notification (non bloquante pour la requête)
    background_tasks.add_task(send_welcome_email, u.email)

    return u

@router.get("", response_model=List[UserRead])
def list_users(_admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(User).all()
