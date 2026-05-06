from .i_metodo_pago import IMetodoPago

class PagoEfectivo(IMetodoPago):
    def procesar_pago(self, monto: float) -> bool:
        # Lógica de tu pago en efectivo
        print(f"Procesando pago en efectivo por el monto de: ${monto}")
        
        # Aquí puedes agregar validaciones. Por ahora retornamos True simulando éxito.
        return True