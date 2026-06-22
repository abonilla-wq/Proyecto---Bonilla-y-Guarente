# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Venta:
    """
    Representa una operacion de venta concretada.
    Consideraciones de eficiencia:
    - O(1) en sus metodos al no depender del tamano de una estructura iterable.
    """
    def __init__(self, producto, id_tarjeta, monto_cobrado):
        """Inicializa la venta guardando referencias O(1)."""
        self.producto = producto
        self.id_tarjeta = id_tarjeta
        self.monto_cobrado = monto_cobrado

    def exportar_a_bd_txt(self):
        """
        Genera el string formateado para el log.
        Eficiencia: O(1) porque interpola strings de longitud fija.
        """
        cod_prod = self.producto.get_cod()
        return f"{self.id_tarjeta},{cod_prod},{self.monto_cobrado}\n"
