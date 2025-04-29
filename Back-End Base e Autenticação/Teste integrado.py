from fastapi.testclient import TestClient
from main import app, Base, engine
import os

# Cria o banco do zero para testar o banco de dados relacional do sistema aplicado.
if os.path.exists("users.db"):
    os.remove("users.db")

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={
        "username": "usuario_teste",
        "password": "senha123"
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "Usuário criado com sucesso"

def test_register_duplicate_user():
    response = client.post("/register", json={
        "username": "usuario_teste",
        "password": "outra_senha"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username já registrado"

def test_login_user():
    response = client.post("/login", json={
        "username": "usuario_teste",
        "password": "senha123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post("/login", json={
        "username": "usuario_teste",
        "password": "senha_errada"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Credenciais inválidas"
