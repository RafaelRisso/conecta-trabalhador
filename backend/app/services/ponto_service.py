from sqlalchemy.orm import Session
from app.models.ponto import Ponto
from typing import List


class PontoService:
    """Serviço responsável pela lógica de marcação de ponto."""

    @staticmethod
    def bater_ponto(db: Session, user_id: int) -> Ponto:
        """
        Registra um ponto de entrada ou saída automaticamente,
        alternando com base no último ponto do usuário.
        """
        ultimo_ponto = (
            db.query(Ponto)
            .filter(Ponto.user_id == user_id)
            .order_by(Ponto.timestamp.desc())
            .first()
        )

        tipo = "entrada"
        if ultimo_ponto and ultimo_ponto.tipo == "entrada":
            tipo = "saida"

        ponto = Ponto(user_id=user_id, tipo=tipo)
        db.add(ponto)
        db.commit()
        db.refresh(ponto)
        return ponto

    @staticmethod
    def listar_pontos(db: Session, user_id: int) -> List[Ponto]:
        """Retorna o histórico de pontos de um usuário."""
        return db.query(Ponto).filter(Ponto.user_id == user_id).all()
