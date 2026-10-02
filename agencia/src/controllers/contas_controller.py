from fastapi import Request, HTTPException
from config import Configuration as config
from model.contas_model import *

def criar_conta(dados: CriarContaIn, req: Request):
    id = dados.id

    state = req.app.state
    contas, relogio, registro, id_agencia = state.contas, state.relogio, state.registro, state.id_agencia

    if config.agencia_responsavel(id) != id_agencia:
        raise HTTPException(status_code=400, detail=f"Erro: conta {id} não pertence a esta agência.")

    if id in contas:
        raise HTTPException(status_code=409, detail="Erro: conta já existe")

    ts = relogio.evento_local()
    contas[dados.id] = {"id": dados.id, "nomeAluno": dados.nome_aluno, "saldo": dados.saldo_inicial}
    registro.registrar("CRIAR_CONTA", ts, dados.model_dump())

    return {"message": "Conta criada."}

def consultar_saldo(req: Request, conta_id: int):
    state = req.app.state
    contas = state.contas
    conta = contas.get(conta_id)

    if not conta:
        raise HTTPException(status_code=404, detail="Erro: conta não encontrada nesta agência.")
    return conta

def depositar(dados: DepositarIn, req: Request):
    id = dados.id
    valor = dados.valor

    state = req.app.state
    contas, relogio, registro = state.contas, state.relogio, state.registro

    conta = contas.get(id)

    if not conta:
        raise HTTPException(status_code=404, detail="Erro: conta não encontrada nesta agência.")

    ts = relogio.evento_local()
    conta.saldo += valor
    registro.registrar('DEPOSITO', ts, dados.model_dump())

    return conta