# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Producto:
    """
    Clase que representa un producto en la maquina expendedora.
    Consideraciones de eficiencia:
    - La inicializacion y acceso a atributos es O(1) ya que son asignaciones directas en memoria.
    """
    def __init__(self, cod, nombre, precio, despedida, coordenada, stock_actual):
        """Inicializa un producto. Eficiencia: O(1)"""
        self.cod = cod
        self.nombre = nombre
        self.precio = precio
        self.despedida = despedida
        self.coordenada = coordenada
        self.stock_actual = stock_actual

    def get_cod(self):
        """Retorna el codigo. Eficiencia: O(1)"""
        return self.cod

    def set_cod(self, cod):
        """Modifica el codigo. Eficiencia: O(1)"""
        self.cod = cod

    def get_nombre(self):
        """Retorna el nombre. Eficiencia: O(1)"""
        return self.nombre

    def set_nombre(self, nombre):
        """Modifica el nombre. Eficiencia: O(1)"""
        self.nombre = nombre

    def get_precio(self):
        """Retorna el precio. Eficiencia: O(1)"""
        return self.precio

    def set_precio(self, precio):
        """Modifica el precio. Eficiencia: O(1)"""
        self.precio = precio

    def get_despedida(self):
        """Retorna el mensaje de despedida. Eficiencia: O(1)"""
        return self.despedida

    def set_despedida(self, despedida):
        """Modifica el mensaje de despedida. Eficiencia: O(1)"""
        self.despedida = despedida

    def get_coordenada(self):
        """Retorna la coordenada. Eficiencia: O(1)"""
        return self.coordenada

    def set_coordenada(self, coordenada):
        """Modifica la coordenada. Eficiencia: O(1)"""
        self.coordenada = coordenada

    def get_stock_actual(self):
        """Retorna el stock actual. Eficiencia: O(1)"""
        return self.stock_actual

    def set_stock_actual(self, stock_actual):
        """Modifica el stock actual. Eficiencia: O(1)"""
        self.stock_actual = stock_actual

    def descontar_stock(self, cantidad):
        """
        Reduce el stock si es posible.
        Eficiencia: O(1) porque solo compara y resta enteros.
        """
        valido = False
        if self.stock_actual >= cantidad:
            self.stock_actual -= cantidad
            valido = True
        return valido
