from datetime import datetime
from typing import List
from modelos.pelicula import Pelicula
from modelos.sala import Sala
from modelos.asiento import Asiento

class Funcion:
    """
    Clase que representa la proyección de una película en una sala y horario específicos.
    Maneja el estado y contenedor de los asientos para esa instancia específica.
    """
    def __init__(self, fecha_hora: datetime, pelicula: Pelicula, sala: Sala, asientos: List[Asiento]):
        self._fechaHora = fecha_hora
        self._pelicula = pelicula
        self._sala = sala
        self._asientos = asientos

    @property
    def pelicula(self) -> Pelicula:
        return self._pelicula

    @property
    def sala(self) -> Sala:
        return self._sala
        
    @property
    def fechaHora(self) -> datetime:
        return self._fechaHora

    def obtenerAsientosDisponibles(self) -> List[Asiento]:
        """
        Retorna una lista con todos los asientos que no están ocupados actualmente.
        """
        return [asiento for asiento in self._asientos if not asiento.estaOcupado()]

    def marcarAsientoOcupado(self, numero: str) -> None:
        """
        Busca un asiento por su número y cambia su estado a ocupado.
        """
        for asiento in self._asientos:
            if asiento.numero == numero:
                asiento.set_ocupado(True)
                break

    def liberarAsiento(self, numero: str) -> None:
        """
        Busca un asiento por su número y cambia su estado a libre.
        """
        for asiento in self._asientos:
            if asiento.numero == numero:
                asiento.set_ocupado(False)
                break