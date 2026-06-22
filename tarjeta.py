# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Tarjeta:
    """
    Clase que representa una tarjeta de cliente.
    Consideraciones de eficiencia:
    - Todas las operaciones son O(1) ya que manejan acceso y comparaciones directas de datos primitivos.
    """
    def __init__(self, id, saldo):
        """Inicializador. Eficiencia: O(1)"""
        self.id = id
        self.saldo = saldo

    def get_id(self):
        """Retorna el ID. Eficiencia: O(1)"""
        return self.id

    def set_id(self, id):
        """Asigna un ID. Eficiencia: O(1)"""
        self.id = id

    def get_saldo(self):
        """Retorna el saldo actual. Eficiencia: O(1)"""
        return self.saldo

    def set_saldo(self, saldo):
        """Establece un nuevo saldo. Eficiencia: O(1)"""
        self.saldo = saldo

    def descontar_saldo(self, monto):
        """
        Resta el monto del saldo si hay fondos suficientes.
        Eficiencia: O(1) al ser una operacion logica y aritmetica simple.
        """
        valido = False
        if self.saldo >= monto:
            self.saldo -= monto
            valido = True
        return valido
