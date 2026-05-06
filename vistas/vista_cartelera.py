import customtkinter as ctk
import json
import os

class VistaCartelera(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pack_forget()

        # --- NUEVO HEADER SUPERIOR ---
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(fill="x", padx=20, pady=10)

        self.lbl_bienvenida = ctk.CTkLabel(self.frame_header, text="Bienvenido", font=("Arial", 16, "bold"))
        self.lbl_bienvenida.pack(side="left")

        self.btn_logout = ctk.CTkButton(self.frame_header, text="Cerrar Sesión", fg_color="red", hover_color="darkred", width=100, command=self.controlador.cerrar_sesion)
        self.btn_logout.pack(side="right", padx=5)

        self.btn_mis_reservas = ctk.CTkButton(self.frame_header, text="Ver Mis Reservas", fg_color="#1f538d", width=120, command=self.controlador.mostrar_mis_reservas)
        self.btn_mis_reservas.pack(side="right", padx=5)
        # -----------------------------

        self.label_titulo = ctk.CTkLabel(self, text="Cartelera de Cine", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

        self.contenedor_peliculas = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.contenedor_peliculas.pack(pady=10, padx=20, fill="both", expand=True)

    def actualizar_bienvenida(self, nombre_usuario):
        self.lbl_bienvenida.configure(text=f"Hola, {nombre_usuario}")

    def cargar_peliculas(self):
        """Lee el JSON y actualiza la vista dinámica de la cartelera."""
        # Limpiar los widgets anteriores para evitar duplicados al actualizar
        for widget in self.contenedor_peliculas.winfo_children():
            widget.destroy()

        ruta_json = os.path.join("datos", "peliculas.json")
        
        # Validación de existencia del archivo
        if not os.path.exists(ruta_json):
            ctk.CTkLabel(self.contenedor_peliculas, text="Error: No se encontró el archivo peliculas.json").pack(pady=20)
            return

        try:
            with open(ruta_json, "r", encoding="utf-8") as archivo:
                peliculas = json.load(archivo)
                
            if not peliculas:
                ctk.CTkLabel(self.contenedor_peliculas, text="La cartelera está vacía en este momento.").pack(pady=20)
                return

            # Generar las tarjetas de las películas
            for pelicula in peliculas:
                frame_peli = ctk.CTkFrame(self.contenedor_peliculas, corner_radius=10)
                frame_peli.pack(pady=10, padx=10, fill="x")

                titulo = pelicula.get('titulo', 'Sin Título')
                clasificacion = pelicula.get('clasificacion', 'N/A')
                duracion = pelicula.get('duracion', '-- min')

                info_texto = f"{titulo} | {duracion} | {clasificacion}"
                lbl_info = ctk.CTkLabel(frame_peli, text=info_texto, font=("Arial", 16, "bold"))
                lbl_info.pack(anchor="w", padx=15, pady=(10, 5))

                #lbl_sinopsis = ctk.CTkLabel(frame_peli, text=pelicula.get('sinopsis', 'Sin sinopsis disponible.'), wraplength=500, justify="left")
                #lbl_sinopsis.pack(anchor="w", padx=15, pady=5)

                # El botón delega la acción al controlador para cambiar a VistaReserva
                btn_reservar = ctk.CTkButton(frame_peli, text="Ver y Reservar", 
                                             command=lambda p=pelicula: self.controlador.mostrar_reserva(p))
                btn_reservar.pack(anchor="e", padx=15, pady=(5, 10))

        except json.JSONDecodeError:
            ctk.CTkLabel(self.contenedor_peliculas, text="Error: El formato de peliculas.json no es válido.", text_color="red").pack(pady=20)