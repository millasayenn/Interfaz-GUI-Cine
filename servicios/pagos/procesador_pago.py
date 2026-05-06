from .i_metodo_pago import IMetodoPago

"""El ProcesadorPago tiene una variable que guarda cualquier metodo de pago
No le importa si es tarjeta o efectivo, solo sabe que lo que sea que tiene guardado
tiene un metodo llamado procesarCobro()"""

class ProcesadorPago:
    def __init__(self, metodo_pago):
        # Recibe la clase de pago (Tarjeta o Efectivo) y la guarda
        self.metodo_pago = metodo_pago

    def procesar_pago(self, monto):
        # Llama a la función de pago correspondiente. 
        # (Nota: Asegúrate de que tus archivos pago_tarjeta.py y pago_efectivo.py 
        # tengan una función llamada 'procesar_pago' o cambia este nombre según corresponda).
        return self.metodo_pago.procesar_pago(monto)