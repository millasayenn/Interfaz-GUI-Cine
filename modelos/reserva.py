from datetime import date
from typing import List
from modelos.cliente import Cliente
from modelos.asiento import Asiento

class Reserva:
    def __init__(self, id_reserva: int, fecha_creacion: date, monto_total: float, estado: str, cliente: Cliente, asientos_reservados: List[Asiento], sala: str = "Sala 1", cant_adultos: int = 0, cant_ninos: int = 0):
        self._idReserva = id_reserva
        self._fechaCreacion = fecha_creacion
        self._montoTotal = monto_total
        self._estado = estado
        self._cliente = cliente
        self._asientosReservados = asientos_reservados
        self._sala = sala
        self._cant_adultos = cant_adultos
        self._cant_ninos = cant_ninos

    @property
    def idReserva(self) -> int:
        return self._idReserva

    @property
    def estado(self) -> str:
        return self._estado

    def generarComprobante(self) -> str:
        numeros_asientos = ", ".join([asiento.numero for asiento in self._asientosReservados])
        comprobante = (
            f"--- COMPROBANTE DE RESERVA ---\n"
            f"ID Reserva: {self._idReserva}\n"
            f"Cliente: {self._cliente.nombre} ({self._cliente.email})\n"
            f"Fecha de Creación: {self._fechaCreacion}\n"
            f"Sala: {self._sala}\n"
            f"Entradas: {self._cant_adultos} Adultos | {self._cant_ninos} Niños\n"
            f"Asientos: {numeros_asientos}\n"
            f"Monto Total: ${self._montoTotal:.2f}\n"
            f"Estado: {self._estado}\n"
            f"------------------------------"
        )
        return comprobante

    def cambiarEstado(self, nuevo_estado: str) -> None:
        self._estado = nuevo_estado