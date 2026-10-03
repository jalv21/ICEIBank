from pydantic import BaseModel

class TransferenciaIn(BaseModel):
    id_origem: int
    id_destino: int
    valor: float

class CreditarIn(BaseModel):
    valor: float
    id_origem: int
    timestamp: str
