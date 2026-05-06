from .pago_tarjeta import PagoTarjeta
from .pago_efectivo import PagoEfectivo

class FabricaPago:
    @staticmethod
    def crear_pago(tipo):
        # Convertimos a minúsculas por seguridad
        tipo = tipo.lower()
        if tipo == "tarjeta":
            return PagoTarjeta()
        elif tipo == "efectivo":
            return PagoEfectivo()
        else:
            raise ValueError(f"El método de pago '{tipo}' no está soportado.")