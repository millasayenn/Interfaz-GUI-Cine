class Pelicula:
    """
    Clase que representa una película disponible en la cartelera.
    """
    def __init__(self, titulo: str, duracion_minutos: int, clasificacion: str):
        self._titulo = titulo
        self._duracionMinutos = duracion_minutos
        self._clasificacion = clasificacion

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def duracionMinutos(self) -> int:
        return self._duracionMinutos

    @property
    def clasificacion(self) -> str:
        return self._clasificacion