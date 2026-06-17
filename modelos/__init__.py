from .cliente import Cliente
from .pelicula import Pelicula
from .sala import Sala
from .asiento import Asiento
from .funcion import Funcion
from .reserva import Reserva
from .genero import ComponenteGenero, GeneroSimple, CategoriaGenero

# __all__ define explícitamente qué clases se exportan cuando alguien importa el paquete
__all__ = [
    "Cliente",
    "Pelicula",
    "Sala",
    "Asiento",
    "Funcion",
    "Reserva",
    "ComponenteGenero",
    "GeneroSimple",
    "CategoriaGenero"
]