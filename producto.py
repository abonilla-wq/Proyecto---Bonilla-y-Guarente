# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Producto:
    def __init__(self, cod, nombre, precio, despedida, coordenada, stock_actual):
        self.cod = cod
        self.nombre = nombre
        self.precio = precio
        self.despedida = despedida
        self.coordenada = coordenada
        self.stock_actual = stock_actual

    def get_cod(self):
        return self.cod

    def set_cod(self, cod):
        self.cod = cod

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

    def get_despedida(self):
        return self.despedida

    def set_despedida(self, despedida):
        self.despedida = despedida

    def get_coordenada(self):
        return self.coordenada

    def set_coordenada(self, coordenada):
        self.coordenada = coordenada

    def get_stock_actual(self):
        return self.stock_actual

    def set_stock_actual(self, stock_actual):
        self.stock_actual = stock_actual

    def descontar_stock(self, cantidad):
        valido = False
        if self.stock_actual >= cantidad:
            self.stock_actual -= cantidad
            valido = True
        return valido
