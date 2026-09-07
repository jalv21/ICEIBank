from pydantic import BaseModel, EmailStr

class ContaBase(BaseModel):
    nomeAluno: str
    email: EmailStr
    saldo: float

class ContaCreate(ContaBase):
    pass

class ContaResponse(ContaBase):
    id: int

class Config:
    from_attributes = True
