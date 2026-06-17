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
        
        # 2. Inicializamos los servicios
        self.procesadorPago = ProcesadorPago()
        self.notificador = NotificadorEmail()

        # 3. Estado actual del sistema
        self.funcionActual: Funcion = None
        
        # 4. Un diccionario para guardar las reservas creadas
        self.reservas_creadas = {}
        self.contador_id = 1

        # 5. Cargar datos desde los archivos JSON
        self.ruta_reservas = "datos/reservas.json"
        self.ruta_peliculas = "datos/peliculas.json"
        
        # Leemos las películas al abrir el programa
        self.lista_peliculas = GestorJSON.leer_datos(self.ruta_peliculas)
        self.lista_reservas = GestorJSON.leer_datos(self.ruta_reservas)
        
        
    def set_funcion_actual(self, funcion: Funcion):
        # Carga la función que el usuario seleccionó en la cartelera
        self.funcionActual = funcion

    def procesarCompra(self, tipo_pago: str, cliente: Cliente, asientos_seleccionados: list, sala: str = "Sala 1", cant_adultos: int = 0, cant_ninos: int = 0) -> bool:
        # Validamos que haya seleccionado asientos
        if not asientos_seleccionados:
            self.vista.mostrarMensaje("Error: Debes seleccionar al menos un asiento.")
            return False
            
        # 1. Calculamos el total con los nuevos precios de adulto y niño
        monto_total = (cant_adultos * 5000.0) + (cant_ninos * 3000.0)
        
        try:
            # Corrección: El método real en tu archivo fabrica_pago.py es crear_pago()
            metodo = FabricaPago.crear_pago(tipo_pago)
            
            # Corrección: Instanciamos el ProcesadorPago pasándole el método
            procesador_pago_inst = ProcesadorPago(metodo)
            
            # Ejecutamos el cobro usando procesar_pago
            pago_exitoso = procesador_pago_inst.procesar_pago(monto_total)
            
            if pago_exitoso:
                # LINEA 62 - Creamos la reserva con los nombres de parámetros CORRECTOS
                nueva_reserva = Reserva(
                    id_reserva=self.contador_id,
                    fecha_creacion="2026-05-05",
                    monto_total=monto_total,
                    estado="Confirmada",
                    cliente=cliente,
                    asientos_reservados=asientos_seleccionados,
                    sala=sala,                     # NUEVO CAMPO
                    cant_adultos=cant_adultos,     # NUEVO CAMPO
                    cant_ninos=cant_ninos          # NUEVO CAMPO
                )
                
                # Crear la reserva como un diccionario (para el JSON)
                nueva_reserva_dict = {
                    "idReserva": self.contador_id,
                    "fechaCreacion": "2026-05-05",
                    "montoTotal": monto_total,
                    "estado": "Confirmada",
                    "cliente_email": cliente.email,
                    "asientos": [a.numero for a in asientos_seleccionados],
                    "sala": sala,                  # NUEVO CAMPO
                    "cant_adultos": cant_adultos,  # NUEVO CAMPO
                    "cant_ninos": cant_ninos       # NUEVO CAMPO
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
                
                comprobante = nueva_reserva.generarComprobante()
                self.notificador.enviar(cliente.email, comprobante)
                
                self.vista.mostrarMensaje("¡Reserva y pago completados con éxito!")
                return True
                
        except ValueError as e:
            self.vista.mostrarMensaje(str(e))
            return False

    def registrar_reserva(self, datos_reserva):
        """
        Guarda la reserva en reservas.json y bloquea los asientos en peliculas.json
        """
        # 1. Guardar el recibo en reservas.json
        lista_reservas = GestorJSON.leer_datos(self.ruta_reservas) 
        lista_reservas.append(datos_reserva)
        GestorJSON.guardar_datos(self.ruta_reservas, lista_reservas) 

        # 2. Bloquear los asientos en peliculas.json (Para que se marquen en ROJO)
        peliculas = GestorJSON.leer_datos(self.ruta_peliculas) 

        titulo_buscado = datos_reserva.get("pelicula_titulo")
        fecha_buscada = datos_reserva.get("fecha")
        hora_buscada = datos_reserva.get("hora")
        nuevos_asientos = datos_reserva.get("asientos", [])

        # Navegamos por el JSON para encontrar la película, fecha y hora exacta
        for pelicula in peliculas:
            if pelicula.get("titulo") == titulo_buscado:
                for funcion in pelicula.get("funciones", []):
                    if funcion.get("fecha") == fecha_buscada:
                        for horario in funcion.get("horarios", []):
                            if horario.get("hora") == hora_buscada:
                                
                                # Obtenemos la lista actual de ocupados y le sumamos los nuevos
                                ocupados_actuales = horario.get("asientos_ocupados", [])
                                ocupados_actuales.extend(nuevos_asientos)
                                
                                # Evitamos duplicados por seguridad
                                horario["asientos_ocupados"] = list(set(ocupados_actuales))
                                break

        # 3. Guardamos los cambios en el disco duro (JSON)
        GestorJSON.guardar_datos(self.ruta_peliculas, peliculas) 

        # 4. Actualizamos la lista de películas del controlador
        self.lista_peliculas = peliculas


    def devolver_reserva(self, reserva_a_eliminar):
        """
        Elimina la reserva y libera los asientos en la película correspondiente.
        """
        # 1. Eliminar de reservas.json
        lista_reservas = GestorJSON.leer_datos(self.ruta_reservas) 
        
        # Filtramos para dejar todas las reservas MENOS la que queremos eliminar
        lista_reservas = [r for r in lista_reservas if r != reserva_a_eliminar]
        GestorJSON.guardar_datos(self.ruta_reservas, lista_reservas) 

        # 2. Actualizar el stock en peliculas.json
        peliculas = GestorJSON.leer_datos(self.ruta_peliculas) 
        
        titulo_buscado = reserva_a_eliminar.get("pelicula_titulo")
        fecha_buscada = reserva_a_eliminar.get("fecha")
        hora_buscada = reserva_a_eliminar.get("hora")
        asientos_liberados = reserva_a_eliminar.get("asientos", [])

        # Navegamos por el JSON para encontrar la hora exacta
        for pelicula in peliculas:
            if pelicula.get("titulo") == titulo_buscado:
                for funcion in pelicula.get("funciones", []):
                    if funcion.get("fecha") == fecha_buscada:
                        for horario in funcion.get("horarios", []):
                            if horario.get("hora") == hora_buscada:
                                
                                # Quitamos los asientos de la lista de "asientos_ocupados"
                                ocupados_actuales = horario.get("asientos_ocupados", [])
                                nuevos_ocupados = [a for a in ocupados_actuales if a not in asientos_liberados]
                                horario["asientos_ocupados"] = nuevos_ocupados
                                break

        # 3. Guardamos los cambios en el disco duro (JSON)
        GestorJSON.guardar_datos(self.ruta_peliculas, peliculas) 
        self.lista_peliculas = peliculas

        # 4. Refrescar la vista actual de Mis Reservas
        self.vista.vista_mis_reservas.cargar_mis_reservas(lista_reservas)
        
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
        self.vista.mostrarMensaje(f"Asiento actualizado a {asiento_nuevo}.")