from model.contas_model import ContaRepository
from schemas.conta_schema import ContaCreate, ContaUpdate, ContaPartialUpdate
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

    @staticmethod
    def editar_conta_total(conta_id: int, dados: ContaUpdate):
        return ContaRepository.editar(conta_id, dados.model_dump())

    @staticmethod
    def editar_conta_parcial(conta_id: int, dados: ContaPartialUpdate):
        dados_preenchidos = dados.model_dump(exclude_unset=True)
        return ContaRepository.editar(conta_id, dados_preenchidos)