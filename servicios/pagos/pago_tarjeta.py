from .i_metodo_pago import IMetodoPago

class PagoTarjeta(IMetodoPago):
    def procesarCobro(self, monto:float) -> bool:
        print (f"Procesando tarjeta... Cobro de ${monto} con tarjeta exitoso")
        return True
