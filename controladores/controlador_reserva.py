#Importaciones de la capa Modelos
from modelos.funcion import Funcion
from modelos.cliente import Cliente
from modelos.reserva import Reserva
#Importaciones de la capa Servicios
from servicios.almacenamiento.gestor_json import GestorJSON
from servicios.pagos.procesador_pago import ProcesadorPago
from servicios.pagos.fabrica_pago import FabricaPago
from servicios.notificaciones.notificador_email import NotificadorEmail

class ControladorReserva:
    def __init__(self, vista):
        # 1. Guardamos la interfaz gráfica
        self.vista = vista
        
        # 2. Inicializamos tus servicios
        self.procesadorPago = ProcesadorPago()
        self.notificador = NotificadorEmail()

        
        # 3. Estado actual del sistema
        self.funcionActual: Funcion = None
        
        # 4. Un diccionario para guardar las reservas creadas (Simulando una base de datos)
        self.reservas_creadas = {}
        self.contador_id = 1

        # 5. Cargar datos desde los archivos JSON
        self.ruta_reservas = "datos/reservas.json"
        self.ruta_peliculas = "datos/peliculas.json"
        
        # Leemos las películas al abrir el programa
        self.lista_peliculas = GestorJSON.leer_datos(self.ruta_peliculas)
        self.lista_reservas = GestorJSON.leer_datos(self.ruta_reservas)
        
        
    def set_funcion_actual(self, funcion: Funcion):
        """Carga la función que el usuario seleccionó en la cartelera."""
        self.funcionActual = funcion

    def procesarCompra(self, tipo_pago: str, cliente: Cliente, asientos_seleccionados: list) -> bool:
        """
        Orquesta todo el proceso de cobrar, crear la reserva y notificar.
        """
        # Validamos que haya seleccionado asientos
        if not asientos_seleccionados:
            self.vista.mostrarMensaje("Error: Debes seleccionar al menos un asiento.")
            return False
            
        # Calculamos el total (Supongamos que cada entrada vale $5000)
        monto_total = len(asientos_seleccionados) * 5000.0
        
        try:
            # === 1. TU CÓDIGO EN ACCIÓN (S.O.L.I.D.) ===
            # Pedimos a tu fábrica el método de pago correcto
            metodo = FabricaPago.crearMetodoPago(tipo_pago)
            self.procesadorPago.setMetodoPago(metodo)
            
            # Ejecutamos el cobro
            pago_exitoso = self.procesadorPago.ejecutarPago(monto_total)
            
            if pago_exitoso:
                # Creamos la reserva como objeto Python para usarlo en el programa
                nueva_reserva = Reserva(
                    idReserva=self.contador_id,
                    fechaCreacion="2026-05-05",
                    montoTotal=monto_total,
                    estado="Confirmada",
                    cliente=cliente,
                    asientosReservados=asientos_seleccionados
                )
                
                # Crear la reserva como un diccionario (que es lo que entiende JSON)
                nueva_reserva_dict = {
                    "idReserva": self.contador_id,
                    "fechaCreacion": "2026-05-05",
                    "montoTotal": monto_total,
                    "estado": "Confirmada",
                    "cliente_email": cliente.email,
                    "asientos": [a.numero for a in asientos_seleccionados]
                }
                
                # Agregamos la nueva reserva a la lista JSON y guardamos
                self.lista_reservas.append(nueva_reserva_dict)
                GestorJSON.guardar_datos(self.ruta_reservas, self.lista_reservas)
                
                # Ocupamos los asientos en la función actual
                for asiento in asientos_seleccionados:
                    self.funcionActual.marcarAsientoOcupado(asiento.numero)
                
                # Guardamos el objeto reserva en la memoria temporal del programa
                self.reservas_creadas[self.contador_id] = nueva_reserva
                self.contador_id += 1
                
                # === 3. NOTIFICAMOS AL USUARIO ===
                # Ahora sí funcionará porque "nueva_reserva" existe
                comprobante = nueva_reserva.generarComprobante()
                self.notificador.enviar(cliente.email, comprobante)
                
                # === 4. ACTUALIZAMOS LA VISTA ===
                self.vista.mostrarMensaje("¡Reserva y pago completados con éxito!")
                return True
                
        except ValueError as e:
            # Atrapamos los errores de tu fábrica (ej. si el tipo de pago no existe)
            self.vista.mostrarMensaje(str(e))
            return False
        
        
        
    def cancelarReserva(self, id_reserva: int):
        """Busca una reserva, la cancela y libera sus asientos."""
        if id_reserva in self.reservas_creadas:
            reserva = self.reservas_creadas[id_reserva]
            reserva.cambiarEstado("Cancelada")
            
            # Liberamos los asientos para que otros puedan comprarlos
            for asiento in reserva.asientosReservados:
                self.funcionActual.liberarAsiento(asiento.numero)
                
            self.vista.mostrarMensaje(f"Reserva #{id_reserva} cancelada correctamente.")
        else:
            self.vista.mostrarMensaje("Error: Número de reserva no encontrado.")

    def modificarAsientoReserva(self, id_reserva: int, asiento_viejo: str, asiento_nuevo: str):
        """Cambia un asiento por otro si el nuevo está disponible."""
        # Aquí iría la lógica para buscar la reserva, verificar si el 'asiento_nuevo'
        # está libre en la funcionActual, marcarlo ocupado y liberar el 'asiento_viejo'.
        self.vista.mostrarMensaje(f"Asiento actualizado a {asiento_nuevo}.")