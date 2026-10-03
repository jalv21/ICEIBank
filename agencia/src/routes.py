from fastapi import APIRouter

from controllers import contas_controller as contas
from controllers import transferencias_controller as transferencias

router = APIRouter()

router.add_api_route("/contas", contas.criar_conta, methods=["POST"], status_code=201)
router.add_api_route("/contas/{id}", contas.consultar_saldo, methods=["GET"], status_code=200)
router.add_api_route("/contas/{id}/depositar", contas.depositar, methods=["POST"], status_code=200)
router.add_api_route("/contas/{id}/sacar", contas.sacar, methods=["POST"])

router.add_api_route("/transferencias", transferencias.transferir, methods=["POST"], status_code=201)
router.add_api_route("/transferencias/{id}/creditar-remoto", transferencias.creditar_remoto, methods=["POST"], status_code=200)