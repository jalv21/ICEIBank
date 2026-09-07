from model.contas_model import ContaRepository
from schemas.conta_schema import ContaCreate
from config import Configuration

class ContasController:
    @staticmethod
    def listar_contas():
        return ContaRepository.listar()

    @staticmethod
    def buscar_conta(conta_id: int):
        return ContaRepository.buscar_por_id(conta_id)

    @staticmethod
    def criar_conta(conta: ContaCreate):
        return ContaRepository.criar(nome=conta.nomeAluno, email=conta.email, saldo=conta.saldo)

    @staticmethod
    def deletar_conta(conta_id: int):
        return ContaRepository.deletar(conta_id)