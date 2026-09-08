from pydantic import BaseModel
from itertools import count

class ContaModel(BaseModel):
    id: int
    nomeAluno: str
    email: str
    saldo: float

class ContaRepository:
    _contas: list[ContaModel] = []
    _id_counter = count(1)

    @classmethod
    def listar(cls) -> list[ContaModel]:
        return cls._contas

    @classmethod
    def buscar_por_id(cls, conta_id: int) -> ContaModel | None:
        return next((c for c in cls._contas if c.id == conta_id))

    @classmethod
    def criar(cls, nome: str, email: str, saldo: float) -> ContaModel:
        nova_conta = ContaModel(id=next(cls._id_counter), nomeAluno=nome, email=email, saldo=saldo)
        cls._contas.append(nova_conta)
        return nova_conta

    @classmethod
    def deletar(cls, conta_id: int) -> bool:
        conta = cls.buscar_por_id(conta_id)
        if conta:
            cls._contas.remove(conta)
            return True
        return False

    @classmethod
    def editar(cls, conta_id: int, dados: dict) -> ContaModel | None:
        conta = cls.buscar_por_id(conta_id)
        if not conta:
            return None

        conta_atualizada = conta.model_copy(update=dados)

        index = cls._contas.index(conta)
        cls._contas[index] = conta_atualizada
        return conta_atualizada