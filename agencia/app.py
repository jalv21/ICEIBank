from fastapi import FastAPI
from view import contas_view

app = FastAPI(title="ICEIBank - API REST MVC")

app.include_router(contas_view.router)

@app.get("/")
def root():
    return {"mensagem": "API OK"}