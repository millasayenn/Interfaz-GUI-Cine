from .i_metodo_pago import IMetodoPago

class PagoTarjeta(IMetodoPago):
    def procesar_pago(self, monto: float) -> bool:
        # Lógica de tu pago en tarjeta
        print(f"Procesando pago en tarjeta por el monto de: ${monto}")
        
        # Aquí puedes agregar validaciones. Por ahora retornamos True simulando éxito.
        return True