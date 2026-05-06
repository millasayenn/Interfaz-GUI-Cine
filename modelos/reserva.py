from datetime import date
from typing import List
from modelos.cliente import Cliente
from modelos.asiento import Asiento

class Reserva:
    """
    Clase que agrupa los datos de una transacción de reserva realizada por un cliente.
    """
    def __init__(self, id_reserva: int, fecha_creacion: date, monto_total: float, estado: str, cliente: Cliente, asientos_reservados: List[Asiento]):
        self._idReserva = id_reserva
        self._fechaCreacion = fecha_creacion
        self._montoTotal = monto_total
        self._estado = estado
        self._cliente = cliente
        self._asientosReservados = asientos_reservados

    @property
    def idReserva(self) -> int:
        return self._idReserva

    @property
    def estado(self) -> str:
        return self._estado

    def generarComprobante(self) -> str:
        """
        Genera una cadena de texto formateada que sirve como comprobante de la reserva.
        """
        numeros_asientos = ", ".join([asiento.numero for asiento in self._asientosReservados])
        comprobante = (
            f"--- COMPROBANTE DE RESERVA ---\n"
            f"ID Reserva: {self._idReserva}\n"
            f"Cliente: {self._cliente.nombre} ({self._cliente.email})\n"
            f"Fecha de Creación: {self._fechaCreacion}\n"
            f"Asientos: {numeros_asientos}\n"
            f"Monto Total: ${self._montoTotal:.2f}\n"
            f"Estado: {self._estado}\n"
            f"------------------------------"
        )
        return comprobante

    def cambiarEstado(self, nuevo_estado: str) -> None:
        """
        Actualiza el estado de la reserva (ej. 'Pendiente', 'Pagada', 'Cancelada').
        """
        self._estado = nuevo_estado