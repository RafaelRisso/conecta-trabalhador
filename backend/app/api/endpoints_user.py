from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.post("/criar")
def criar_usuario(name: str, db: Session = Depends(get_db)):
    """
    Cria um novo usuário para registrar pontos.
    """
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}
