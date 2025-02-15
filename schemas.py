from pydantic import BaseModel
from typing import List, Optional

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id: int
    class Config:
        from_attributes = True

class ObrigacaoBase(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int

class ObrigacaoCreate(ObrigacaoBase):
    pass

class ObrigacaoResponse(ObrigacaoBase):
    id: int
    class Config:
        from_attributes = True
