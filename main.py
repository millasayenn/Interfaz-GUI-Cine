import customtkinter as ctk

# ==========================================
# IMPORTACIONES (Descomentar a medida que se creen los archivos)
# ==========================================
# from vistas.vista_reserva import VistaReserva
# from controladores.controlador_reserva import ControladorReserva

def main():
    # 1. Configuración global de la interfaz
    ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

    # 2. Crear la ventana principal
    ventana_principal = ctk.CTk()
    ventana_principal.title("Cine TPA - Sistema de Reservas")
    ventana_principal.geometry("900x600")
    
    # 3. Instanciar la Vista
    # Le pasamos la ventana principal a la vista para que sepa dónde dibujar los botones
    # vista_reserva = VistaReserva(root=ventana_principal)
    
    # 4. Instanciar el Controlador
    # Le pasamos la vista al controlador para que pueda escuchar los clics
    # controlador = ControladorReserva(vista=vista_reserva)

    # 5. Iniciar el programa (esto mantiene la ventana abierta)
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()
