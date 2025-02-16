from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Função para obter sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint raiz
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de gerenciamento de empresas e obrigações acessórias!"}

# Criar uma empresa
@app.post("/empresas/", response_model=schemas.Empresa, status_code=status.HTTP_201_CREATED)
def criar_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    # Verifica se o CNPJ já está cadastrado
    db_empresa = db.query(models.Empresa).filter(models.Empresa.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    # Cria a empresa
    db_empresa = models.Empresa(**empresa.model_dump())  # Substitui .dict() por .model_dump()
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

# Listar empresas
@app.get("/empresas/", response_model=list[schemas.Empresa])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(models.Empresa).all()

# Buscar empresa por ID
@app.get("/empresas/{empresa_id}", response_model=schemas.Empresa)
def buscar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

# Criar obrigação acessória
@app.post("/obrigacoes/", response_model=schemas.ObrigacaoAcessoria, status_code=status.HTTP_201_CREATED)
def criar_obrigacao(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    # Verifica se a empresa associada existe
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == obrigacao.empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    # Cria a obrigação
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())  # Substitui .dict() por .model_dump()
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao