from fastapi import APIRouter

from controllers import contas_controller as contas

router = APIRouter()

router.add_api_route("/contas", contas.criar_conta, methods=["POST"], status_code=201)
router.add_api_route("/contas/{id}", contas.consultar_saldo, methods=["GET"], status_code=200)
router.add_api_route("/contas/{id}", contas.depositar, methods=["POST"], status_code=200)