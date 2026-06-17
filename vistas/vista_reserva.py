import customtkinter as ctk
from tkinter import messagebox

# Importamos tu módulo de pagos
from servicios.pagos.fabrica_pago import FabricaPago
from servicios.pagos.procesador_pago import ProcesadorPago

class VistaReserva(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pelicula_actual = None
        self.funciones_actuales = []
        self.asientos_seleccionados = []
        
        self.pack_forget()

        self.label_titulo = ctk.CTkLabel(self, text="Reserva de Asientos", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

        # Panel de información de la película
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(pady=5, padx=20, fill="x")

        self.lbl_peli_titulo = ctk.CTkLabel(self.info_frame, text="", font=("Arial", 18, "bold"))
        self.lbl_peli_titulo.pack(pady=2)

        self.lbl_peli_detalles = ctk.CTkLabel(self.info_frame, text="")
        self.lbl_peli_detalles.pack(pady=2)

        # --- Selector de Fecha y Hora ---
        self.frame_selectores = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_selectores.pack(pady=10)

        # Fecha
        self.lbl_fecha = ctk.CTkLabel(self.frame_selectores, text="Fecha:")
        self.lbl_fecha.grid(row=0, column=0, padx=5)
        self.cb_fecha = ctk.CTkComboBox(self.frame_selectores, state="readonly", command=self.al_seleccionar_fecha)
        self.cb_fecha.grid(row=0, column=1, padx=5)
        self.cb_fecha.configure(state="disabled")

        # Hora (Añadimos el command aquí)
        self.lbl_hora = ctk.CTkLabel(self.frame_selectores, text="Hora:")
        self.lbl_hora.grid(row=0, column=2, padx=5)
        self.cb_hora = ctk.CTkComboBox(self.frame_selectores, state="readonly", command=self.al_seleccionar_hora)
        self.cb_hora.grid(row=0, column=3, padx=5)
        self.cb_hora.configure(state="disabled")

        # Idioma
        self.lbl_idioma = ctk.CTkLabel(self.frame_selectores, text="Idioma:")
        self.lbl_idioma.grid(row=0, column=4, padx=5)
        self.cb_idioma = ctk.CTkComboBox(self.frame_selectores, state="readonly", command=self.al_seleccionar_idioma)
        self.cb_idioma.grid(row=0, column=5, padx=5)
        self.cb_idioma.configure(state="disabled")

        # --- Cuadrícula de Asientos ---
        ctk.CTkLabel(self, text="Seleccione sus asientos (Gris: Disponible | Rojo: Ocupado):", font=("Arial", 14)).pack(pady=5)
        
        self.asientos_frame = ctk.CTkFrame(self)
        self.asientos_frame.pack(pady=5, padx=20)
        self.botones_asientos = {}

        # --- Botones de Acción ---
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=15)

        self.btn_pagar = ctk.CTkButton(self.frame_botones, text="Proceder al Pago", fg_color="green", hover_color="darkgreen", command=self.iniciar_pago)
        self.btn_pagar.pack(side="left", padx=10)

        self.btn_volver = ctk.CTkButton(self.frame_botones, text="Cancelar y Volver", fg_color="red", hover_color="darkred", command=self.volver_cartelera)
        self.btn_volver.pack(side="left", padx=10)

    def actualizar_informacion(self, pelicula):
        self.pelicula_actual = pelicula 
        self.asientos_seleccionados.clear()

        # Limpiar la cuadrícula porque aún no hay fecha ni hora elegida
        self.limpiar_cuadricula()

        if isinstance(pelicula, dict):
            titulo = pelicula.get('titulo', 'Sin título')
            self.funciones_actuales = pelicula.get('funciones', [])
        else:
            titulo = getattr(pelicula, 'titulo', 'Sin título')
            self.funciones_actuales = getattr(pelicula, 'funciones', [])

        self.lbl_peli_titulo.configure(text=titulo)

        # Extraer fechas
        fechas_disponibles = []
        for funcion in self.funciones_actuales:
            f_fecha = funcion.get('fecha') if isinstance(funcion, dict) else getattr(funcion, 'fecha', '')
            if f_fecha:
                fechas_disponibles.append(f_fecha)

        fechas_unicas = list(dict.fromkeys(fechas_disponibles))

        if fechas_unicas:
            self.cb_fecha.configure(values=fechas_unicas, state="readonly")
            self.cb_fecha.set("Seleccione una fecha...")
        else:
            self.cb_fecha.configure(values=["No hay funciones"], state="disabled")
            self.cb_fecha.set("No hay funciones")

        self.cb_hora.configure(values=[""], state="disabled")
        self.cb_hora.set("")

        # Agrega esto:
        self.cb_idioma.configure(values=[""], state="disabled")
        self.cb_idioma.set("")

    def al_seleccionar_fecha(self, fecha_seleccionada):
        """Busca los horarios para la fecha y limpia los asientos"""
        self.limpiar_cuadricula() # Ocultar asientos hasta que elija hora
        self.cb_idioma.configure(values=[""], state="disabled")
        self.cb_idioma.set("")
        horas_disponibles = []
        
        for funcion in self.funciones_actuales:
            f_fecha = funcion.get('fecha') if isinstance(funcion, dict) else getattr(funcion, 'fecha', '')
            
            if f_fecha == fecha_seleccionada:
                # Ahora leemos "horarios" en lugar de "horas"
                horarios = funcion.get('horarios', []) if isinstance(funcion, dict) else getattr(funcion, 'horarios', [])
                for h in horarios:
                    hora_str = h.get('hora') if isinstance(h, dict) else getattr(h, 'hora', '')
                    if hora_str:
                        horas_disponibles.append(hora_str)

        horas_unicas = list(dict.fromkeys([h for h in horas_disponibles if h]))

        if horas_unicas:
            self.cb_hora.configure(values=horas_unicas, state="readonly")
            self.cb_hora.set("Seleccione una hora...")
        else:
            self.cb_hora.configure(values=["Sin horas"], state="disabled")
            self.cb_hora.set("Sin horas")

    def al_seleccionar_hora(self, hora_seleccionada):
        """Habilita la selección de idioma al escoger una hora y limpia la cuadrícula."""
        self.limpiar_cuadricula()
        
        # Como ahora todas las funciones tienen Doblada y Subtitulada:
        self.cb_idioma.configure(values=["Doblada", "Subtitulada"], state="readonly")
        self.cb_idioma.set("Seleccione idioma...")

    def al_seleccionar_idioma(self, idioma_seleccionado):
        """Busca los asientos ocupados específicos para la fecha, hora e IDIOMA seleccionado."""
        fecha_seleccionada = self.cb_fecha.get()
        hora_seleccionada = self.cb_hora.get()
        asientos_ocupados = []

        for funcion in self.funciones_actuales:
            f_fecha = funcion.get('fecha') if isinstance(funcion, dict) else getattr(funcion, 'fecha', '')
            
            if f_fecha == fecha_seleccionada:
                horarios = funcion.get('horarios', []) if isinstance(funcion, dict) else getattr(funcion, 'horarios', [])
                for h in horarios:
                    h_str = h.get('hora') if isinstance(h, dict) else getattr(h, 'hora', '')
                    if h_str == hora_seleccionada:
                        # Buscamos en la nueva estructura de idiomas:
                        idiomas = h.get('idiomas', {})
                        asientos_ocupados = idiomas.get(idioma_seleccionado, [])
                        break
        
        self.generar_cuadricula_asientos(asientos_ocupados)

    def limpiar_cuadricula(self):
        """Elimina los botones de la cuadrícula visualmente"""
        self.asientos_seleccionados.clear()
        for widget in self.asientos_frame.winfo_children():
            widget.destroy()
        self.botones_asientos.clear()

    def generar_cuadricula_asientos(self, asientos_ocupados):
        self.limpiar_cuadricula()

        for f in range(5):
            for c in range(6):
                num_asiento = f"{chr(65+f)}{c+1}"
                btn = ctk.CTkButton(self.asientos_frame, text=num_asiento, width=45, height=45)
                
                if num_asiento in asientos_ocupados:
                    btn.configure(fg_color="red", state="disabled")
                else:
                    btn.configure(fg_color="gray", hover_color="lightgray", 
                                  command=lambda a=num_asiento: self.seleccionar_asiento(a))
                
                btn.grid(row=f, column=c, padx=5, pady=5)
                self.botones_asientos[num_asiento] = btn

    def seleccionar_asiento(self, asiento):
        if asiento in self.asientos_seleccionados:
            self.asientos_seleccionados.remove(asiento)
            self.botones_asientos[asiento].configure(fg_color="gray")
        else:
            self.asientos_seleccionados.append(asiento)
            self.botones_asientos[asiento].configure(fg_color="#1f538d")

    def iniciar_pago(self):
        if self.cb_fecha.get() == "Seleccione una fecha..." or self.cb_fecha.get() == "No hay funciones":
            messagebox.showwarning("Faltan datos", "Debe seleccionar una fecha.")
            return
            
        if self.cb_hora.get() == "Seleccione una hora..." or self.cb_hora.get() == "" or self.cb_hora.get() == "Sin horas":
            messagebox.showwarning("Faltan datos", "Debe seleccionar una hora.")
            return

        if not self.asientos_seleccionados:
            messagebox.showwarning("Sin asientos", "Debe seleccionar al menos un asiento para reservar.")
            return
        
        self.ventana_pago = ctk.CTkToplevel(self)
        self.ventana_pago.title("Proceso de Pago")
        self.ventana_pago.geometry("400x420")
        self.ventana_pago.attributes("-topmost", True)
        self.ventana_pago.grab_set() 

        ctk.CTkLabel(self.ventana_pago, text="Pasarela de Pago", font=("Arial", 20, "bold")).pack(pady=10)
        
        cantidad_asientos = len(self.asientos_seleccionados)
        ctk.CTkLabel(self.ventana_pago, text=f"Asientos seleccionados: {cantidad_asientos}", font=("Arial", 14)).pack(pady=5)

        # --- SELECCIÓN DE ENTRADAS (Adultos/Niños) ---
        self.precio_adulto = 5000
        self.precio_nino = 3000
        self.total = cantidad_asientos * self.precio_adulto 

        self.cant_adultos_var = ctk.StringVar(value=str(cantidad_asientos))
        self.cant_ninos_var = ctk.StringVar(value="0")

        frame_entradas = ctk.CTkFrame(self.ventana_pago, fg_color="transparent")
        frame_entradas.pack(pady=10)

        opciones = [str(i) for i in range(cantidad_asientos + 1)] 

        ctk.CTkLabel(frame_entradas, text="Adultos ($5000):").grid(row=0, column=0, padx=5, pady=5)
        self.cb_adultos = ctk.CTkComboBox(frame_entradas, values=opciones, variable=self.cant_adultos_var, command=self.al_cambiar_adultos, width=80)
        self.cb_adultos.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_entradas, text="Niños ($3000):").grid(row=1, column=0, padx=5, pady=5)
        self.cb_ninos = ctk.CTkComboBox(frame_entradas, values=opciones, variable=self.cant_ninos_var, command=self.al_cambiar_ninos, width=80)
        self.cb_ninos.grid(row=1, column=1, padx=5, pady=5)
        # ---------------------------------------------

        # --- ESTA ES LA PARTE QUE SE HABÍA BORRADO ---
        self.lbl_total = ctk.CTkLabel(self.ventana_pago, text=f"Total a Pagar: ${self.total}", font=("Arial", 16, "bold"))
        self.lbl_total.pack(pady=10)

        self.metodo_pago = ctk.CTkComboBox(self.ventana_pago, values=["tarjeta", "efectivo"], state="readonly")
        self.metodo_pago.pack(pady=10)

        ctk.CTkButton(self.ventana_pago, text="Confirmar y Pagar", fg_color="green", command=self.finalizar_reserva).pack(pady=10)
        ctk.CTkButton(self.ventana_pago, text="Cancelar", fg_color="red", command=self.ventana_pago.destroy).pack(pady=5)

    def al_cambiar_adultos(self, valor):
        """Calcula automáticamente la cantidad de niños si cambia la de adultos"""
        try:
            adultos = int(valor)
            total_asientos = len(self.asientos_seleccionados)
            ninos = total_asientos - adultos
            self.cant_ninos_var.set(str(ninos)) # Actualiza la barra de niños
            self.actualizar_total(None)         # Recalcula el dinero
        except ValueError:
            pass

    def al_cambiar_ninos(self, valor):
        """Calcula automáticamente la cantidad de adultos si cambia la de niños"""
        try:
            ninos = int(valor)
            total_asientos = len(self.asientos_seleccionados)
            adultos = total_asientos - ninos
            self.cant_adultos_var.set(str(adultos)) # Actualiza la barra de adultos
            self.actualizar_total(None)             # Recalcula el dinero
        except ValueError:
            pass

    def actualizar_total(self, _):
        """Calcula el precio en tiempo real cuando se cambian los selectores"""
        try:
            adultos = int(self.cant_adultos_var.get())
            ninos = int(self.cant_ninos_var.get())
            self.total = (adultos * self.precio_adulto) + (ninos * self.precio_nino)
            self.lbl_total.configure(text=f"Total a Pagar: ${self.total}")
        except ValueError:
            pass

    def finalizar_reserva(self):
        # 1. Validar que las entradas coincidan con los asientos
        try:
            adultos = int(self.cant_adultos_var.get())
            ninos = int(self.cant_ninos_var.get())
        except ValueError:
            return

        if (adultos + ninos) != len(self.asientos_seleccionados):
            messagebox.showwarning("Error de Entradas", f"Debe asignar exactamente {len(self.asientos_seleccionados)} entrada(s) en total.")
            return

        tipo_seleccionado = self.metodo_pago.get()

        try:
            metodo = FabricaPago.crear_pago(tipo_seleccionado) 
            procesador = ProcesadorPago(metodo)
            procesador.procesar_pago(self.total)
        except Exception as e:
            messagebox.showerror("Error de Pago", f"Hubo un error con la pasarela: {str(e)}")
            return

        titulo = self.pelicula_actual.get("titulo") if isinstance(self.pelicula_actual, dict) else getattr(self.pelicula_actual, "titulo", "Desconocido")
        sala_asignada = "Sala 1" # Aquí asignamos la sala que se guardará

        # Al guardar este diccionario, main.py lo incrustará automáticamente en reservas.json
        datos_reserva = {
            "pelicula_titulo": titulo,
            "sala": sala_asignada, 
            "fecha": self.cb_fecha.get(),
            "hora": self.cb_hora.get(),
            "idioma": self.cb_idioma.get(),
            "asientos": self.asientos_seleccionados,
            "cant_adultos": adultos,
            "cant_ninos": ninos,
            "metodo_pago": tipo_seleccionado,
            "total": self.total
        }

        self.ventana_pago.destroy() 
        self.controlador.registrar_reserva(datos_reserva)
        
        # Boleta actualizada
        detalle_ticket = (
            f"Película: {titulo}\n"
            f"Sala: {sala_asignada}\n"
            f"Fecha: {self.cb_fecha.get()}\n"
            f"Hora: {self.cb_hora.get()}\n"
            f"Idioma: {self.cb_idioma.get()}\n"
            f"Asientos: {', '.join(self.asientos_seleccionados)}\n"
            f"Entradas: {adultos} Adulto(s) | {ninos} Niño(s)\n"
            f"Total Pagado: ${self.total} ({tipo_seleccionado.capitalize()})"
        )
        messagebox.showinfo("¡Reserva Confirmada!", detalle_ticket)
        self.volver_cartelera()

    def volver_cartelera(self):
        self.controlador.mostrar_cartelera()