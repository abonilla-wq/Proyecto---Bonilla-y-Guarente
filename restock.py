# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Restock:
    def __init__(self, cod_producto, cantidad, fecha_hora):
        self.cod_producto = cod_producto
        self.cantidad = cantidad
        self.fecha_hora = fecha_hora

    def exportar_a_bd_txt(self):
        return f"{self.fecha_hora},{self.cod_producto},{self.cantidad}\n"
