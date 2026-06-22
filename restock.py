# Integrantes: Ariadna Bonilla, Isabella Guarente.

class Restock:
    """
    Registra operaciones de llenado o modificacion de la maquina.
    Consideraciones de eficiencia:
    - Asignaciones e interpolaciones O(1).
    """
    def __init__(self, cod_producto, cantidad, fecha_hora):
        """Constructor. Eficiencia: O(1)"""
        self.cod_producto = cod_producto
        self.cantidad = cantidad
        self.fecha_hora = fecha_hora

    def exportar_a_bd_txt(self):
        """
        Formatea el registro para guardado.
        Eficiencia: O(1)
        """
        return f"{self.fecha_hora},{self.cod_producto},{self.cantidad}\n"
