from pydantic import BaseModel, EmailStr
from typing import Optional

class ContaBase(BaseModel):
    nomeAluno: str
    email: EmailStr
    saldo: float

class ContaCreate(ContaBase):
    pass

class ContaResponse(ContaBase):
    id: int

class ContaUpdate(ContaBase):
    pass

class ContaPartialUpdate(BaseModel):
    nomeAluno: Optional[str] = None
    email: Optional[EmailStr] = None

class Config:
    from_attributes = True