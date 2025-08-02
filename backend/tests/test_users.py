def test_criar_usuario(client):
    response = client.post(
        "/auth/register?name=Tester&email=tester@example.com&password=123456"
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "tester@example.com"


def test_register_and_login(client):
    # Registro
    client.post("/auth/register?name=User1&email=user1@example.com&password=secret")
    
    # Login
    response_login = client.post(
        "/auth/login",
        data={"username": "user1@example.com", "password": "secret"}
    )
    assert response_login.status_code == 200
    token_data = response_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
