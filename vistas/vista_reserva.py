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

    def al_seleccionar_fecha(self, fecha_seleccionada):
        """Busca los horarios para la fecha y limpia los asientos"""
        self.limpiar_cuadricula() # Ocultar asientos hasta que elija hora
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
        """Busca los asientos ocupados específicos para la fecha y hora seleccionada"""
        fecha_seleccionada = self.cb_fecha.get()
        asientos_ocupados = []

        for funcion in self.funciones_actuales:
            f_fecha = funcion.get('fecha') if isinstance(funcion, dict) else getattr(funcion, 'fecha', '')
            
            if f_fecha == fecha_seleccionada:
                horarios = funcion.get('horarios', []) if isinstance(funcion, dict) else getattr(funcion, 'horarios', [])
                for h in horarios:
                    h_str = h.get('hora') if isinstance(h, dict) else getattr(h, 'hora', '')
                    if h_str == hora_seleccionada:
                        asientos_ocupados = h.get('asientos_ocupados', []) if isinstance(h, dict) else getattr(h, 'asientos_ocupados', [])
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
        self.ventana_pago.geometry("400x300")
        self.ventana_pago.attributes("-topmost", True)
        self.ventana_pago.grab_set() 

        ctk.CTkLabel(self.ventana_pago, text="Pasarela de Pago", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.total = len(self.asientos_seleccionados) * 5000
        ctk.CTkLabel(self.ventana_pago, text=f"Total a Pagar: ${self.total}", font=("Arial", 16)).pack(pady=10)

        self.metodo_pago = ctk.CTkComboBox(self.ventana_pago, values=["tarjeta", "efectivo"], state="readonly")
        self.metodo_pago.pack(pady=10)

        ctk.CTkButton(self.ventana_pago, text="Confirmar y Pagar", fg_color="green", command=self.finalizar_reserva).pack(pady=10)
        ctk.CTkButton(self.ventana_pago, text="Cancelar", fg_color="red", command=self.ventana_pago.destroy).pack(pady=5)

    def finalizar_reserva(self):
        tipo_seleccionado = self.metodo_pago.get()

        try:
            metodo = FabricaPago.crear_pago(tipo_seleccionado) 
            procesador = ProcesadorPago(metodo)
            procesador.procesar_pago(self.total)
            
        except Exception as e:
            messagebox.showerror("Error de Pago", f"Hubo un error con la pasarela: {str(e)}")
            return

        titulo = self.pelicula_actual.get("titulo") if isinstance(self.pelicula_actual, dict) else getattr(self.pelicula_actual, "titulo", "Desconocido")

        datos_reserva = {
            "pelicula_titulo": titulo,
            "fecha": self.cb_fecha.get(),
            "hora": self.cb_hora.get(),
            "asientos": self.asientos_seleccionados,
            "metodo_pago": tipo_seleccionado,
            "total": self.total
        }

        # 1. Destruimos la ventana de pago
        self.ventana_pago.destroy() 
        
        # 2. Registramos la reserva UNA SOLA VEZ
        self.controlador.registrar_reserva(datos_reserva)
        
        # 3. Armamos y mostramos el ticket
        detalle_ticket = (
            f"Película: {titulo}\n"
            f"Fecha: {self.cb_fecha.get()}\n"
            f"Hora: {self.cb_hora.get()}\n"
            f"Asientos: {', '.join(self.asientos_seleccionados)}\n"
            f"Total Pagado: ${self.total} ({tipo_seleccionado.capitalize()})"
        )
        messagebox.showinfo("¡Reserva Confirmada!", detalle_ticket)
        
        # 4. Volvemos al inicio
        self.volver_cartelera()

    def volver_cartelera(self):
        self.controlador.mostrar_cartelera()