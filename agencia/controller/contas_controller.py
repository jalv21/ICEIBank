from fastapi import Request, status, HTTPException
from pydantic import BaseModel
import config
import app

class ContaBody(BaseModel):
    id: int
    nomeAluno: str
    saldoInicial: str

@app.post("/contas")
async def criar_conta(dados: ContaBody, request: Request):
    id = dados.id
    nome_aluno = dados.nomeAluno
    saldo_inicial = dados.saldoInicial

    contas = request.app.state.contas
    relogio = request.app.state.relogio
    registro = request.app.state.registro
    id_agencia = request.app.state.idAgencia

    if(config.agencia_responsavel(id) != id_agencia):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Conta {id} não pertence a esta agência."
        )

    if id in contas:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Esta conta já existe."
        )

    ts = relogio.evento_local()
    contas[id] = {
        "id": id,
        "nomeAluno": nome_aluno,
        "saldo": saldo_inicial or 0
    }

    registro.registrar('CRIAR_CONTA', ts, { id, nome_aluno, saldo_inicial })

    return status.HTTP_201_CREATED