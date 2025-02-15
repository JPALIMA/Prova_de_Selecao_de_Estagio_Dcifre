from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_criar_empresa():
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "12345678000100",
        "endereco": "Rua X, 123",
        "email": "teste@email.com",
        "telefone": "999999999"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"
