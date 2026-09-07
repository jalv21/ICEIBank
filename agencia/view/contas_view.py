from fastapi import APIRouter, HTTPException
from agencia.controller.contas_controller import ContasController
from agencia.schemas.conta_schema import ContaCreate, ContaResponse

router = APIRouter(prefix="/contas", tags=["Contas"])

@router.get("/", response_model=list[ContaResponse])
def listar():
    return ContasController.listar_contas()

@router.get("/{conta_id}", response_model=ContaResponse)
def buscar(conta_id: int):
    conta = ContasController.buscar_conta(conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    return conta

@router.post("/", reponse_model=ContaResponse, status_code=201)
def criar(conta: ContaCreate):
    return ContasController.criar_conta(conta)

@router.delete("/{usuario_id}")
def deletar(conta_id: int):
    success = ContasController.deletar_conta(conta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Aluno não encontado")
    return {"detail": "Conta removida com sucesso"}