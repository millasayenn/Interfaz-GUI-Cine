from .i_metodo_pago import IMetodoPago

class ProcesadorPago:
    def __init__(self, metodo_pago: IMetodoPago):
        # Recibe la clase de pago instanciada (Tarjeta o Efectivo) y la guarda
        self.metodo_pago = metodo_pago

    def procesar_pago(self, monto: float) -> bool:
        # Llama a la función de pago correspondiente usando el nombre estandarizado
        return self.metodo_pago.procesar_pago(monto)