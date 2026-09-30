from fastapi import FastAPI
from config import Configuration as config
from services.log_eventos import RegistroEventos
from services.relogio_lamport import RelogioLamport
from contextlib import asynccontextmanager
import os
import sys
from urllib.parse import urlparse
from routes import router

id_agencia = int(os.environ.get("AGENCIA_ID", "0"))
agencia_config = next((a for a in config.AGENCIAS if a["id"] == id_agencia))

if not agencia_config:
    print(f"Agência {id_agencia} não configurada em config.py", file=sys.stderr)
    sys.exit(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.id_agencia = id_agencia
    app.state.relogio = RelogioLamport()
    app.state.registro = RegistroEventos()
    app.state.contas = {}

    porta = urlparse(agencia_config.url).port
    print(f"[Agência {id_agencia}] ouvindo na porta {porta}")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

