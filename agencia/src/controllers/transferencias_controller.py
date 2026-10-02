from fastapi import Request
from model.transferencias_model import *

async def transferir(dados: TransferenciaIn, req: Request):
    state = req.app.state
    contas, relogio, registro, id_agencia = state.contas, state.relogio, state.registro, state.id_agencia

    id_origem = dados.id_origem
    id_destino = dados.id_destino
    valor = dados.valor

    conta_origem = contas.get(id_origem)