from .i_metodo_pago import IMetodoPago

"""El ProcesadorPago tiene una variable que guarda cualquier metodo de pago
No le importa si es tarjeta o efectivo, solo sabe que lo que sea que tiene guardado
tiene un metodo llamado procesarCobro()"""

class ProcesadorPago:
    def __init__(self):
        self.estrategiaPago: IMetodoPago = None

    def setMetodoPago(self, metodo: IMetodoPago):
        #Asigna el método de pago que utilizará"
        self.estrategiaPago = metodo
    def ejecutarPago(self, monto: float) -> bool:
        #Ejecuta el cobro usando la estrategia asignada
        if self.estrategiaPago is None:
            raise Exception ("No se ha definido un método de pago antes de cobrar")
        return self.estrategiaPago.procesarCobro(monto)