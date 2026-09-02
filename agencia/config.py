class Configuration:
    def __init__(self):
        self.OFFSET = 42
        self.NUMERO_AGENCIAS = 3
        self.PORTA_BASE = 4000 + self.OFFSET
        self.AGENCIAS = [
            { "id": 0, "url": f"http://localhost={self.PORTA_BASE}"},
            { "id": 1, "url": f"http://localhost={self.PORTA_BASE + 1}"},
            { "id": 2, "url": f"http://localhost={self.PORTA_BASE + 2}"}
        ]

    def agencia_responsavel(self, idConta: int):
        return idConta % self.NUMERO_AGENCIAS
