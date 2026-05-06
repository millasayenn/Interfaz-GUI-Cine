from .i_metodo_pago import IMetodoPago

class PagoEfectivo(IMetodoPago):
    def procesarCobro(self, monto:float) -> bool:
        print (f"Cajero recibe efectivo. Cobro de ${monto} exitoso")
        return True
        