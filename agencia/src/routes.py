from fastapi import APIRouter

from controllers import contas_controller as contas

router = APIRouter()

router.add_api_route("/contas", contas.criar_conta, methods=["POST"], status_code=201)