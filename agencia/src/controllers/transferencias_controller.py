from fastapi import Request, HTTPException
from model.transferencias_model import *
from config import Configuration as config

async def transferir(dados: TransferenciaIn, req: Request):
    state = req.app.state
    contas, relogio, registro, id_agencia = state.contas, state.relogio, state.registro, state.id_agencia

    id_origem = dados.id_origem
    id_destino = dados.id_destino
    valor = dados.valor

    conta_origem = contas.get(id_origem)

    if not conta_origem:
        raise HTTPException(status_code=404, detail="Conta de origem não encontrada na agência")

    if conta_origem.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    agencia_destino = config.agencia_responsavel(id_destino)

    # Débito sempre local, pois a agência é dona da conta de origem
    ts_debito = relogio.evento_local()
    conta_origem.saldo -= valor
    registro.registrar('TRANSFERENCIA_DEBITO', ts_debito, dados.model_dump())

    if agencia_destino == id_agencia:
        conta_destino = contas.get(id_destino)

        if not conta_destino:
            conta_origem.saldo += valor
            raise HTTPException(status_code=404, detail="Erro: Conta de destino não encontrada")
        
        ts_credito = relogio.evento_local()
        conta_destino.saldo += valor
        registro.registrar('TRANSFERENCIA_CREDITO', ts_credito, dados.model_dump())


