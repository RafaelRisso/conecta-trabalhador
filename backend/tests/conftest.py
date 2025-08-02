import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.models.user import User  # força carregamento
from app.models.ponto import Ponto  # força carregamento

# Banco de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database_once():
    """Cria as tabelas uma vez para todos os testes."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    """Cliente de teste usando DB em memória."""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    """Cria usuário e retorna token JWT."""
    client.post("/auth/register?name=Tester&email=test@example.com&password=123456")
    response = client.post(
        "/auth/login", 
        data={"username": "test@example.com", "password": "123456"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]
