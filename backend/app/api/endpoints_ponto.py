from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.ponto_service import PontoService
from app.services.auth_service import AuthService
from app.models.user import User
from app.db.session import get_db

router = APIRouter(prefix="/ponto", tags=["Ponto"])


@router.post("/bater")
def bater_ponto(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """
    Endpoint para bater ponto (entrada/saída).
    Requer autenticação com JWT.
    """
    ponto = PontoService.bater_ponto(db, current_user.id)
    return {
        "id": ponto.id,
        "tipo": ponto.tipo,
        "timestamp": ponto.timestamp
    }


@router.get("/historico")
def historico(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """
    Lista o histórico de pontos de um usuário autenticado.
    """
    pontos = PontoService.listar_pontos(db, current_user.id)
    return [
        {"id": p.id, "tipo": p.tipo, "timestamp": p.timestamp}
        for p in pontos
    ]
