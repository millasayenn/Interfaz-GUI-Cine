from abc import ABC, abstractmethod

class EstadoPelicula(ABC):
    @abstractmethod
    def puede_reservar(self) -> bool:
        pass
    
    @abstractmethod
    def obtener_mensaje(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class EnCartelera(EstadoPelicula):
    def puede_reservar(self) -> bool:
        return True
        
    def obtener_mensaje(self) -> str:
        return "Reserva disponible."
        
    def __str__(self) -> str:
        return "En Cartelera"

class Proximamente(EstadoPelicula):
    def puede_reservar(self) -> bool:
        return False
        
    def obtener_mensaje(self) -> str:
        return "Aún no disponible. ¡Próximamente!"
        
    def __str__(self) -> str:
        return "Próximamente"

class Archivada(EstadoPelicula):
    def puede_reservar(self) -> bool:
        return False
        
    def obtener_mensaje(self) -> str:
        return "Película fuera de cartelera."
        
    def __str__(self) -> str:
        return "Archivada"