# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Tarjeta:
    def __init__(self, id, saldo):
        self.id = id
        self.saldo = saldo

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_saldo(self):
        return self.saldo

    def set_saldo(self, saldo):
        self.saldo = saldo

    def descontar_saldo(self, monto):
        valido = False
        if self.saldo >= monto:
            self.saldo -= monto
            valido = True
        return valido
