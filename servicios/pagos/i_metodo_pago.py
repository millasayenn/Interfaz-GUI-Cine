from abc import ABC, abstractmethod

class IMetodoPago(ABC):
    @abstractmethod
    def procesar_pago(self, monto: float) -> bool:
        """
        Procesa el pago. Debe ser implementado por las clases hijas.
        Retorna True si el pago es exitoso, False en caso contrario.
        """
        pass