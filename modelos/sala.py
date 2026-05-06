class Sala:
    """
    Clase que representa una sala física del cine.
    """
    def __init__(self, numero: int, capacidad: int):
        self._numero = numero
        self._capacidad = capacidad

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def capacidad(self) -> int:
        return self._capacidad