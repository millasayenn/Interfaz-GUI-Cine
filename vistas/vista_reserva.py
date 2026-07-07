import customtkinter as ctk
from tkinter import messagebox
import os
from servicios.pagos.fabrica_pago import FabricaPago
from servicios.pagos.procesador_pago import ProcesadorPago

class VistaReserva(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pelicula_actual = None
        self.funciones_actuales = []
        self.asientos_seleccionados = []
        self.sala_asignada = "Sala 1"
        
        self.pack_forget()

        self.label_titulo = ctk.CTkLabel(self, text="Reserva de Asientos", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(15, 5))

        # ==========================================
        #       LAYOUT PRINCIPAL DE DOS COLUMNAS
        # ==========================================
        self.frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

        # ------------------------------------------
        # COLUMNA IZQ: PÓSTER E INFORMACIÓN
        # ------------------------------------------
        self.frame_izq = ctk.CTkFrame(self.frame_principal, fg_color="transparent", width=250)
        self.frame_izq.pack(side="left", fill="y", padx=(0, 20))

        # Etiqueta para la imagen
        self.lbl_imagen = ctk.CTkLabel(self.frame_izq, text="")
        self.lbl_imagen.pack(pady=(0, 10))

        # Título de la película
        self.lbl_peli_titulo = ctk.CTkLabel(self.frame_izq, text="", font=("Arial", 20, "bold"), wraplength=250, justify="center")
        self.lbl_peli_titulo.pack(pady=2)

        # Detalles técnicos (duración, género, clasif)
        self.lbl_peli_detalles = ctk.CTkLabel(self.frame_izq, text="", font=("Arial", 13), text_color="#2daae1", wraplength=250, justify="center")
        self.lbl_peli_detalles.pack(pady=2)

        # Sinopsis
        self.lbl_sinopsis = ctk.CTkLabel(self.frame_izq, text="", font=("Arial", 12), text_color="gray", wraplength=250, justify="left")
        self.lbl_sinopsis.pack(pady=(15, 0), anchor="n", fill="x")


        # ------------------------------------------
        # COLUMNA DER: SELECTORES Y ASIENTOS
        # ------------------------------------------
        self.frame_der = ctk.CTkFrame(self.frame_principal, fg_color="#1a1a1a", corner_radius=15)
        self.frame_der.pack(side="right", fill="both", expand=True, ipadx=10, ipady=10)

        self.frame_selectores = ctk.CTkFrame(self.frame_der, fg_color="transparent")
        self.frame_selectores.pack(pady=15)

        self.lbl_fecha = ctk.CTkLabel(self.frame_selectores, text="Fecha:", font=("Arial", 13, "bold"))
        self.lbl_fecha.grid(row=0, column=0, padx=5)
        self.cb_fecha = ctk.CTkComboBox(self.frame_selectores, state="readonly", command=self.al_seleccionar_fecha, width=130)
        self.cb_fecha.grid(row=0, column=1, padx=5)
        self.cb_fecha.configure(state="disabled")

        self.lbl_hora = ctk.CTkLabel(self.frame_selectores, text="Hora:", font=("Arial", 13, "bold"))
        self.lbl_hora.grid(row=0, column=2, padx=5)
        self.cb_hora = ctk.CTkComboBox(self.frame_selectores, state="readonly", command=self.al_seleccionar_hora, width=110)
        self.cb_hora.grid(row=0, column=3, padx=5)
        self.cb_hora.configure(state="disabled")

        self.lbl_idioma = ctk.CTkLabel(self.frame_selectores, text="Idioma:", font=("Arial", 13, "bold"))
        self.lbl_idioma.grid(row=0, column=4, padx=5)
        self.cb_idioma = ctk.CTkComboBox(self.frame_selectores, state="readonly", command=self.al_seleccionar_idioma, width=120)
        self.cb_idioma.grid(row=0, column=5, padx=5)
        self.cb_idioma.configure(state="disabled")

        # Indicador de sala dinámica
        self.lbl_info_sala = ctk.CTkLabel(self.frame_der, text="Por favor, seleccione fecha, hora e idioma.", font=("Arial", 14, "italic"), text_color="#d48806")
        self.lbl_info_sala.pack(pady=5)

        ctk.CTkLabel(self.frame_der, text="Pantalla / Escenario", font=("Arial", 12), text_color="gray", fg_color="#3b3b3b", width=300, corner_radius=5).pack(pady=(15, 5))

        self.asientos_frame = ctk.CTkFrame(self.frame_der, fg_color="transparent")
        self.asientos_frame.pack(pady=5, padx=20, expand=True)
        self.botones_asientos = {}

        # Botones de Acción (Pagar / Cancelar)
        self.frame_botones = ctk.CTkFrame(self.frame_der, fg_color="transparent")
        self.frame_botones.pack(pady=15, side="bottom")

        self.btn_volver = ctk.CTkButton(self.frame_botones, text="← Volver a Cartelera", fg_color="red", hover_color="darkred", command=self.volver_cartelera)
        self.btn_volver.pack(side="left", padx=10)

        self.btn_pagar = ctk.CTkButton(self.frame_botones, text="Proceder al Pago →", fg_color="green", hover_color="darkgreen", command=self.iniciar_pago)
        self.btn_pagar.pack(side="left", padx=10)

    def actualizar_informacion(self, pelicula):
        self.pelicula_actual = pelicula 
        self.asientos_seleccionados.clear()
        self.limpiar_cuadricula()
        self.lbl_info_sala.configure(text="Por favor, seleccione fecha, hora e idioma.")

        if isinstance(pelicula, dict):
            titulo = pelicula.get('titulo', 'Sin título')
            duracion = pelicula.get('duracion', '-- min')
            clasificacion = pelicula.get('clasificacion', 'N/A')
            genero = pelicula.get('genero', 'Desconocido')
            sinopsis = pelicula.get('sinopsis', 'Sin sinopsis disponible.')
            ruta_imagen = pelicula.get('imagen', '')
            self.funciones_actuales = pelicula.get('funciones', [])
        else:
            titulo = getattr(pelicula, 'titulo', 'Sin título')
            duracion = getattr(pelicula, 'duracion', '-- min')
            clasificacion = getattr(pelicula, 'clasificacion', 'N/A')
            genero = getattr(pelicula, 'genero', 'Desconocido')
            sinopsis = getattr(pelicula, 'sinopsis', 'Sin sinopsis disponible.')
            ruta_imagen = getattr(pelicula, 'imagen', '')
            self.funciones_actuales = getattr(pelicula, 'funciones', [])

        # Actualizar textos de la UI
        self.lbl_peli_titulo.configure(text=titulo)
        self.lbl_peli_detalles.configure(text=f"⏳ {duracion}  |  🎬 {clasificacion}\n🎭 {genero}")
        self.lbl_sinopsis.configure(text=sinopsis)

        # Actualizar Imagen
        if ruta_imagen and os.path.exists(ruta_imagen):
            try:
                from PIL import Image
                img_pil = Image.open(ruta_imagen)
                img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(200, 300))
                self.lbl_imagen.configure(image=img_ctk, text="", fg_color="transparent")
            except Exception as e:
                self.lbl_imagen.configure(image="", text="🎬\nError al cargar póster", font=("Arial", 16), width=200, height=300, fg_color="#2a2a2a", corner_radius=10)
        else:
            self.lbl_imagen.configure(image="", text="🎬\nSin Póster", font=("Arial", 18), width=200, height=300, fg_color="#2a2a2a", corner_radius=10)

        # Configurar Fechas
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
        self.cb_idioma.configure(values=[""], state="disabled")
        self.cb_idioma.set("")

    def al_seleccionar_fecha(self, fecha_seleccionada):
        self.limpiar_cuadricula() 
        self.lbl_info_sala.configure(text="Seleccione ahora la hora.")
        self.cb_idioma.configure(values=[""], state="disabled")
        self.cb_idioma.set("")
        horas_disponibles = []
        
        for funcion in self.funciones_actuales:
            f_fecha = funcion.get('fecha') if isinstance(funcion, dict) else getattr(funcion, 'fecha', '')
            
            if f_fecha == fecha_seleccionada:
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
        self.limpiar_cuadricula()
        self.lbl_info_sala.configure(text="Por último, seleccione el idioma.")
        fecha_seleccionada = self.cb_fecha.get()
        idiomas_disp = []
        
        for funcion in self.funciones_actuales:
            if funcion.get('fecha') == fecha_seleccionada:
                for h in funcion.get('horarios', []):
                    if h.get("hora") == hora_seleccionada:
                        if "idioma" in h: 
                            idiomas_disp.append(h["idioma"])
                        elif "idiomas" in h: 
                            idiomas_disp.extend(h["idiomas"].keys())
                            
        idiomas_unicos = list(dict.fromkeys(idiomas_disp))
        
        if idiomas_unicos:
            self.cb_idioma.configure(values=idiomas_unicos, state="readonly")
            self.cb_idioma.set("Seleccione idioma...")
        else:
            self.cb_idioma.configure(values=["Sin idioma"], state="disabled")
            self.cb_idioma.set("Sin idioma")

    def al_seleccionar_idioma(self, idioma_seleccionado):
        fecha_seleccionada = self.cb_fecha.get()
        hora_seleccionada = self.cb_hora.get()
        asientos_ocupados = []
        self.sala_asignada = "Sala 1" 

        for funcion in self.funciones_actuales:
            if funcion.get('fecha') == fecha_seleccionada:
                for h in funcion.get('horarios', []):
                    if h.get('hora') == hora_seleccionada:
                        if "idioma" in h and h["idioma"] == idioma_seleccionado:
                            self.sala_asignada = h.get("sala", "Sala 1")
                            asientos_ocupados = h.get("asientos_ocupados", [])
                            break
                        elif "idiomas" in h:
                            asientos_ocupados = h["idiomas"].get(idioma_seleccionado, [])
                            break
                            
        self.lbl_info_sala.configure(text=f"Proyectándose en: {self.sala_asignada}")
        self.generar_cuadricula_asientos(asientos_ocupados)

    def limpiar_cuadricula(self):
        self.asientos_seleccionados.clear()
        for widget in self.asientos_frame.winfo_children():
            widget.destroy()
        self.botones_asientos.clear()

    def generar_cuadricula_asientos(self, asientos_ocupados):
        import os
        import json
        
        self.limpiar_cuadricula()

        capacidad = 30  
        ruta_salas = os.path.join("datos", "salas.json")
        
        if os.path.exists(ruta_salas):
            try:
                with open(ruta_salas, "r", encoding="utf-8") as f:
                    salas = json.load(f)
                    for s in salas:
                        nombre_completo = f"{s.get('nombre')} ({s.get('tipo')})"
                        if self.sala_asignada == nombre_completo or self.sala_asignada == s.get('nombre'):
                            capacidad = int(s.get("capacidad", 30))
                            break
            except Exception as e:
                print(f"Error al leer capacidad de la sala: {e}")

        if capacidad <= 30:
            columnas = 6
        elif capacidad <= 50:
            columnas = 10
        else:
            columnas = 12

        filas = (capacidad + columnas - 1) // columnas 
        asiento_actual = 0

        for f in range(filas):
            for c in range(columnas):
                if asiento_actual >= capacidad:
                    break 
                
                num_asiento = f"{chr(65+f)}{c+1}"
                btn = ctk.CTkButton(self.asientos_frame, text=num_asiento, width=45, height=45)
                
                if num_asiento in asientos_ocupados:
                    btn.configure(fg_color="#8b0000", hover_color="#8b0000", state="disabled") # Rojo oscuro para asientos ocupados
                else:
                    btn.configure(fg_color="#3b3b3b", hover_color="lightgray",
                                command=lambda a=num_asiento: self.seleccionar_asiento(a))
                
                btn.grid(row=f, column=c, padx=3, pady=3)
                self.botones_asientos[num_asiento] = btn
                asiento_actual += 1

    def seleccionar_asiento(self, asiento):
        if asiento in self.asientos_seleccionados:
            self.asientos_seleccionados.remove(asiento)
            self.botones_asientos[asiento].configure(fg_color="#3b3b3b")
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
            
        if self.cb_idioma.get() == "Seleccione idioma..." or self.cb_idioma.get() == "":
            messagebox.showwarning("Faltan datos", "Debe seleccionar un idioma.")
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

        self.lbl_total = ctk.CTkLabel(self.ventana_pago, text=f"Total a Pagar: ${self.total}", font=("Arial", 16, "bold"))
        self.lbl_total.pack(pady=10)

        self.metodo_pago = ctk.CTkComboBox(self.ventana_pago, values=["tarjeta", "efectivo"], state="readonly")
        self.metodo_pago.pack(pady=10)

        ctk.CTkButton(self.ventana_pago, text="Confirmar y Pagar", fg_color="green", command=self.finalizar_reserva).pack(pady=10)
        ctk.CTkButton(self.ventana_pago, text="Cancelar", fg_color="red", command=self.ventana_pago.destroy).pack(pady=5)

    def al_cambiar_adultos(self, valor):
        try:
            adultos = int(valor)
            total_asientos = len(self.asientos_seleccionados)
            ninos = total_asientos - adultos
            self.cant_ninos_var.set(str(ninos)) 
            self.actualizar_total(None)         
        except ValueError:
            pass

    def al_cambiar_ninos(self, valor):
        try:
            ninos = int(valor)
            total_asientos = len(self.asientos_seleccionados)
            adultos = total_asientos - ninos
            self.cant_adultos_var.set(str(adultos)) 
            self.actualizar_total(None)             
        except ValueError:
            pass

    def actualizar_total(self, _):
        try:
            adultos = int(self.cant_adultos_var.get())
            ninos = int(self.cant_ninos_var.get())
            self.total = (adultos * self.precio_adulto) + (ninos * self.precio_nino)
            self.lbl_total.configure(text=f"Total a Pagar: ${self.total}")
        except ValueError:
            pass

    def finalizar_reserva(self):
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

        datos_reserva = {
            "pelicula_titulo": titulo,
            "sala": self.sala_asignada, 
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
        
        detalle_ticket = (
            f"Película: {titulo}\n"
            f"Sala: {self.sala_asignada}\n"
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