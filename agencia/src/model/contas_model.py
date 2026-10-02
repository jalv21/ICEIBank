from pydantic import BaseModel

class CriarContaIn(BaseModel):
    id: int
    nome_aluno: str
    email: str
    saldo_inicial: float = 0

class DepositarIn(BaseModel):
    id: int
    valor: float
    novo_saldo: float

class SacarIn(BaseModel):
    id: int
    valor: float
    