import customtkinter as ctk
from tkinter import messagebox

class VistaMisReservas(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pack_forget()

        ctk.CTkLabel(self, text="Mis Reservas", font=("Arial", 24, "bold")).pack(pady=15)

        # Contenedor con scroll para ver todas las reservas
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=350)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.btn_volver = ctk.CTkButton(self, text="Volver a Cartelera", fg_color="gray", 
                                        command=lambda: self.controlador.mostrar_cartelera())
        self.btn_volver.pack(pady=15)

    def cargar_mis_reservas(self, reservas):
        """Limpia la pantalla y dibuja las reservas actuales"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not reservas:
            ctk.CTkLabel(self.scroll_frame, text="No tienes reservas actualmente.", font=("Arial", 14)).pack(pady=20)
            return

        for reserva in reservas:
            # Tarjeta de cada reserva
            frame_reserva = ctk.CTkFrame(self.scroll_frame, fg_color="#2b2b2b")
            frame_reserva.pack(pady=5, padx=5, fill="x")

            detalles = (
                f" {reserva.get('pelicula_titulo')}\n"
                f" {reserva.get('fecha')} | {reserva.get('hora')} | {reserva.get('idioma', 'Doblada')}\n"
                f" Asientos: {', '.join(reserva.get('asientos', []))}"
            )

            lbl_info = ctk.CTkLabel(frame_reserva, text=detalles, justify="left", font=("Arial", 12))
            lbl_info.pack(side="left", padx=10, pady=10)

            # Botón de devolución
            btn_devolver = ctk.CTkButton(frame_reserva, text="Devolver", fg_color="red", hover_color="darkred", width=80,
                                         command=lambda r=reserva: self.solicitar_devolucion(r))
            btn_devolver.pack(side="right", padx=10)

    def solicitar_devolucion(self, reserva):
        respuesta = messagebox.askyesno("Confirmar Devolución", 
                                        f"¿Deseas anular la reserva y liberar los asientos de '{reserva.get('pelicula_titulo')}'?")
        if respuesta:
            # Llama al controlador para hacer la magia de los JSON
            self.controlador.devolver_reserva(reserva)
            messagebox.showinfo("Éxito", "Asientos devueltos. El stock ha sido actualizado.")