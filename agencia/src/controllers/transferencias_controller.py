from fastapi import Request, HTTPException
from model.transferencias_model import *
from config import Configuration as config
import httpx

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

        return {"mensagem": "Transferência concluída (mesma agência)"}

    # Caso entre agências: chama a agência de destino diretamente via REST
    ts_envio = relogio.ao_enviar()
    dados_agencia_destino = next((a for a in config.AGENCIAS if a["id"] == agencia_destino), None)
    url_destino = dados_agencia_destino["url"]

    try:
        async with httpx.AsyncClient() as client:
            resposta = await client.post(
                f"{url_destino}/contas/{id_destino}/creditar-remoto",
                json={
                    "valor": valor,
                    "id_origem": id_origem,
                    "timestamp": ts_envio,
                },
                timeout=10.0,
            )
            resposta.raise_for_status()

        return {"mensagem": "Transferência concluída (entre agências)."}
    
    except httpx.HTTPError as erro:
        # LIMITAÇÃO CONHECIDA: se esta chamada falhar, o débito já aplicado acima
        # NÃO é revertido - o dinheiro "desaparece" temporariamente. Resolver isso
        # de forma correta (garantir atomicidade mesmo sob falha) é o assunto do
        # Sprint 4, com uma transação distribuída de verdade (2PC/Saga). Por
        # enquanto, só registramos a inconsistência no log.
        registro.registrar('TRANSFERENCIA_FALHOU', relogio.evento_local(), dados.model_dump())
        raise HTTPException(
            status_code = 502,
            detail="Falha ao contatar agência de destino. Débito já aplicado - inconsistência conhecida (ver Sprint 4)"
        )

