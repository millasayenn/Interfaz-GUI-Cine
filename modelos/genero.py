from abc import ABC, abstractmethod

class ComponenteGenero(ABC):
    """Componente Base del Patrón Composite"""
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def contiene(self, genero_buscar: str) -> bool:
        """Verifica si el género buscado pertenece a esta categoría o nodo"""
        pass

class GeneroSimple(ComponenteGenero):
    """Hoja (Leaf) - Un género individual sin subcategorías"""
    def contiene(self, genero_buscar: str) -> bool:
        return self.nombre.lower() == genero_buscar.lower()

class CategoriaGenero(ComponenteGenero):
    """Compuesto (Composite) - Una categoría que agrupa subgéneros"""
    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.subgeneros = []

    def agregar(self, componente: ComponenteGenero):
        self.subgeneros.append(componente)

    def eliminar(self, componente: ComponenteGenero):
        self.subgeneros.remove(componente)

    def contiene(self, nombre_genero: str) -> bool:
        # Si la película pertenece exactamente a este género padre, retorna True
        if self.nombre.lower() == nombre_genero.lower():
            return True
        # Si no, busca recursivamente en todos sus subgéneros hijos
        for sub in self.subgeneros:
            if sub.contiene(nombre_genero):
                return True
        return False