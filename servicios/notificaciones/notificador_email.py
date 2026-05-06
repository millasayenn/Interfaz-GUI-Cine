from .i_notificador import INotificador

class NotificadorEmail(INotificador):
    """
    Simulación de un servicio de notificaciones por correo electrónico.
    """
    
    def enviar(self, destinatario: str, mensaje: str) -> bool:
        # Simulamos el envío del correo
        print("\n" + "="*40)
        print("📧 SIMULADOR DE SERVIDOR DE CORREO")
        print("="*40)
        print(f"Enviando a: {destinatario}")
        print("-" * 40)
        print(mensaje)
        print("-" * 40)
        print("✅ Correo enviado exitosamente.")
        print("="*40 + "\n")
        
        return True