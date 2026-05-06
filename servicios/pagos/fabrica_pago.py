from .pago_tarjeta import PagoTarjeta
from .pago_efectivo import PagoEfectivo
from .i_metodo_pago import IMetodoPago

class FabricaPago:
    @staticmethod
    def crearMetodoPago(tipo: str) -> IMetodoPago:
        tipo_limpio = tipo.lower().strip()
        if tipo_limpio == "tarjeta":
            return PagoTarjeta()
        elif tipo_limpio == "efectivo":
            return PagoEfectivo()
        else:
            raise ValueError (f"Error: El tipo de pago {tipo} no existe en el sistema.")
            