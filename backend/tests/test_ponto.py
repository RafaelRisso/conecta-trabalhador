def test_bater_ponto_e_historico(client):
    # Criar usuário
    client.post("/auth/register?name=Funcionario&email=func@example.com&password=123456")
    
    # Login
    response_login = client.post(
        "/auth/login",
        data={"username": "func@example.com", "password": "123456"}
    )
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Bater ponto entrada
    response_ponto1 = client.post("/ponto/bater", headers=headers)
    assert response_ponto1.status_code == 200
    assert response_ponto1.json()["tipo"] == "entrada"

    # Bater ponto saída
    response_ponto2 = client.post("/ponto/bater", headers=headers)
    assert response_ponto2.status_code == 200
    assert response_ponto2.json()["tipo"] == "saida"

    # Histórico deve ter pelo menos 2 pontos
    historico = client.get("/ponto/historico", headers=headers)
    assert historico.status_code == 200
    assert len(historico.json()) >= 2


def test_bater_ponto_usuario_inexistente(client):
    """Testa se token inválido retorna 401"""
    headers = {"Authorization": "Bearer token_invalido"}
    response = client.post("/ponto/bater", headers=headers)
    assert response.status_code == 401
