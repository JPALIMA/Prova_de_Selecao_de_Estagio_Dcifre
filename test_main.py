from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, engine
import models

# Cria as tabelas no banco de dados de teste
models.Base.metadata.create_all(bind=engine)

# Cria uma instância do TestClient
client = TestClient(app)

# Função para limpar o banco de dados antes de cada teste
def limpar_banco_de_dados():
    db = SessionLocal()
    try:
        db.query(models.ObrigacaoAcessoria).delete()
        db.query(models.Empresa).delete()
        db.commit()
    finally:
        db.close()

# Teste para criar uma empresa
def test_criar_empresa():
    # Limpa o banco de dados antes do teste
    limpar_banco_de_dados()

    # Dados da empresa
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "12345678000100",
        "endereco": "Rua X, 123",
        "email": "teste@email.com",
        "telefone": "999999999"
    }

    # Cria a empresa
    response = client.post("/empresas/", json=empresa_data)
    assert response.status_code == 201  # Status code correto para criação
    assert response.json()["nome"] == "Empresa Teste"
    assert response.json()["cnpj"] == "12345678000100"

# Teste para listar empresas
def test_listar_empresas():
    # Limpa o banco de dados antes do teste
    limpar_banco_de_dados()

    # Cria uma empresa para listar
    empresa_data = {
        "nome": "Empresa Listar",
        "cnpj": "98765432000100",
        "endereco": "Rua Y, 456",
        "email": "listar@email.com",
        "telefone": "888888888"
    }
    client.post("/empresas/", json=empresa_data)

    # Lista as empresas
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Empresa Listar"

# Teste para buscar empresa por ID
def test_buscar_empresa():
    # Limpa o banco de dados antes do teste
    limpar_banco_de_dados()

    # Cria uma empresa para buscar
    empresa_data = {
        "nome": "Empresa Buscar",
        "cnpj": "11112222000100",
        "endereco": "Rua Z, 789",
        "email": "buscar@email.com",
        "telefone": "777777777"
    }
    create_response = client.post("/empresas/", json=empresa_data)
    empresa_id = create_response.json()["id"]

    # Busca a empresa criada
    response = client.get(f"/empresas/{empresa_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Buscar"
    assert response.json()["cnpj"] == "11112222000100"

# Teste para criar uma obrigação acessória
def test_criar_obrigacao():
    # Limpa o banco de dados antes do teste
    limpar_banco_de_dados()

    # Cria uma empresa para associar à obrigação
    empresa_data = {
        "nome": "Empresa Obrigação",
        "cnpj": "33334444000100",
        "endereco": "Rua W, 101",
        "email": "obrigacao@email.com",
        "telefone": "666666666"
    }
    empresa_response = client.post("/empresas/", json=empresa_data)
    empresa_id = empresa_response.json()["id"]

    # Cria a obrigação acessória
    obrigacao_data = {
        "nome": "Declaração de Imposto",
        "periodicidade": "mensal",
        "empresa_id": empresa_id
    }
    response = client.post("/obrigacoes/", json=obrigacao_data)
    assert response.status_code == 201
    assert response.json()["nome"] == "Declaração de Imposto"
    assert response.json()["periodicidade"] == "mensal"