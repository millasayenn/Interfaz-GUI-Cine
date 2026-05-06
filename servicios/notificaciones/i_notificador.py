from abc import ABC, abstractmethod

class INotificador(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> bool:
        # Método vacío que las clases hijas deberán implementar obligatoriamente.
        pass