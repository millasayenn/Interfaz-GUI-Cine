class Asiento:
    """
    Clase que representa un asiento individual dentro de una función.
    """
    def __init__(self, numero: str, ocupado: bool = False):
        self._numero = numero
        self._ocupado = ocupado

    @property
    def numero(self) -> str:
        return self._numero

    def estaOcupado(self) -> bool:
        """
        Devuelve el estado actual de ocupación del asiento.
        """
        return self._ocupado

    def set_ocupado(self, estado: bool):
        """
        Actualiza el estado de ocupación del asiento. 
        Método de apoyo para garantizar el correcto encapsulamiento.
        """
        self._ocupado = estado