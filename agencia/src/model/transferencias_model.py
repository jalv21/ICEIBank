from pydantic import BaseModel

class TransferenciaIn(BaseModel):
    id_origem: int
    id_destino: int
    