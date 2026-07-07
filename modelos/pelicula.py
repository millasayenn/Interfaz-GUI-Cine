from modelos.estado_pelicula import EstadoPelicula, EnCartelera, Proximamente, Archivada

class Pelicula:
    def __init__(self, titulo: str, duracion_minutos: str, clasificacion: str, estado_str: str = "En Cartelera"):
        self._titulo = titulo
        self._duracionMinutos = duracion_minutos
        self._clasificacion = clasificacion
        self._estado = self._mapear_estado(estado_str)

    def _mapear_estado(self, estado_str: str) -> EstadoPelicula:
        mapeo = {
            "Próximamente": Proximamente(),
            "En Cartelera": EnCartelera(),
            "Archivada": Archivada()
        }
        return mapeo.get(estado_str, EnCartelera())

    def cambiar_estado(self, nuevo_estado: EstadoPelicula):
        self._estado = nuevo_estado

    def intentar_reserva(self) -> bool:
        """Delega la validación de la reserva a la clase de Estado correspondiente."""
        return self._estado.puede_reservar()
        
    @property
    def estado_actual(self) -> str:
        return str(self._estado)