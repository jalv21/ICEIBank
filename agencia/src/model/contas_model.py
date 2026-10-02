from pydantic import BaseModel

class CriarContaIn(BaseModel):
    id: int
    nome_aluno: str
    email: str
    saldo_inicial: float = 0