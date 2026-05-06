import customtkinter as ctk

class VistaMisReservas(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pack_forget()

        self.label_titulo = ctk.CTkLabel(self, text="Mis Películas Reservadas", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)

        self.contenedor_reservas = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.contenedor_reservas.pack(pady=10, padx=20, fill="both", expand=True)

        self.btn_volver = ctk.CTkButton(self, text="Volver a Cartelera", command=self.controlador.mostrar_cartelera)
        self.btn_volver.pack(pady=20)

    def cargar_mis_reservas(self, reservas_usuario):
        """Renderiza las reservas que el controlador le pasa por parámetro"""
        for widget in self.contenedor_reservas.winfo_children():
            widget.destroy()

        if not reservas_usuario:
            ctk.CTkLabel(self.contenedor_reservas, text="Aún no tienes reservas.", font=("Arial", 16)).pack(pady=20)
            return

        for reserva in reservas_usuario:
            frame_reserva = ctk.CTkFrame(self.contenedor_reservas, corner_radius=10)
            frame_reserva.pack(pady=10, padx=10, fill="x")

            lbl_titulo = ctk.CTkLabel(frame_reserva, text=f"Película: {reserva['pelicula_titulo']}", font=("Arial", 16, "bold"))
            lbl_titulo.pack(anchor="w", padx=15, pady=(10, 2))

            asientos_str = ", ".join(reserva['asientos'])
            lbl_detalles = ctk.CTkLabel(frame_reserva, text=f"Asientos: {asientos_str} | Pagado con: {reserva['metodo_pago']}")
            lbl_detalles.pack(anchor="w", padx=15, pady=(2, 10))