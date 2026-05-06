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

        # (ELIMINAMOS EL FORMULARIO DE CLIENTE DE AQUÍ)

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
        
        self.lbl_peli_titulo.configure(text=pelicula.get("titulo", "Título Desconocido"))
        self.lbl_peli_detalles.configure(text=f"Género: {pelicula.get('genero', '')} | Duración: {pelicula.get('duracion', '')}")
        self.generar_cuadricula_asientos()

    def generar_cuadricula_asientos(self):
        for widget in self.asientos_frame.winfo_children():
            widget.destroy()
        self.botones_asientos.clear()

        asientos_ocupados = self.pelicula_actual.get("asientos_ocupados", [])

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

        # Los values deben coincidir con lo que espera tu 'FabricaPago'
        self.metodo_pago = ctk.CTkComboBox(self.ventana_pago, values=["tarjeta", "efectivo"])
        self.metodo_pago.pack(pady=10)

        ctk.CTkButton(self.ventana_pago, text="Confirmar y Pagar", fg_color="green", command=self.finalizar_reserva).pack(pady=10)
        ctk.CTkButton(self.ventana_pago, text="Cancelar", fg_color="red", command=self.ventana_pago.destroy).pack(pady=5)

    def finalizar_reserva(self):
        tipo_seleccionado = self.metodo_pago.get()

        # --- USO DE LA CARPETA PAGOS ---
        try:
            # 1. Llamamos a la fábrica para crear el método de pago (Ajusta los nombres a tus clases reales)
            metodo = FabricaPago.crear_pago(tipo_seleccionado) 
            
            # 2. Le pasamos el método al procesador
            procesador = ProcesadorPago(metodo)
            
            # 3. Procesamos el pago
            procesador.procesar_pago(self.total)
            
        except Exception as e:
            messagebox.showerror("Error de Pago", f"Hubo un error con la pasarela: {str(e)}")
            return # Detiene la reserva si falla la tarjeta o el efectivo

        # Si el pago pasó, guardamos la reserva (No lleva nombre ni correo aquí)
        datos_reserva = {
            "pelicula_titulo": self.pelicula_actual.get("titulo"),
            "asientos": self.asientos_seleccionados,
            "metodo_pago": tipo_seleccionado
        }

        self.ventana_pago.destroy() 
        self.controlador.registrar_reserva(datos_reserva)
        messagebox.showinfo("Éxito", "¡Pago exitoso! Su reserva ha sido guardada.")
        self.volver_cartelera()

    def volver_cartelera(self):
        self.controlador.mostrar_cartelera()