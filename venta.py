# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Venta:
    def __init__(self, producto, id_tarjeta, monto_cobrado):
        self.producto = producto
        self.id_tarjeta = id_tarjeta
        self.monto_cobrado = monto_cobrado

    def exportar_a_bd_txt(self):
        cod_prod = self.producto.get_cod()
        return f"{self.id_tarjeta},{cod_prod},{self.monto_cobrado}\n"
