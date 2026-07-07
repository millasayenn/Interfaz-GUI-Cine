from abc import ABC, abstractmethod

class ComponenteGenero(ABC):
    """Componente Base del Patrón Composite"""
    def __init__(self, nombre: str):
        self.nombre = nombre

    def _normalizar(self, texto: str) -> str:
        """Elimina mayúsculas y tildes para hacer búsquedas flexibles"""
        t = texto.lower()
        reemplazos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
        for a, b in reemplazos.items():
            t = t.replace(a, b)
        return t

    @abstractmethod
    def contiene(self, genero_buscar: str) -> bool:
        """Verifica si el género buscado pertenece a esta categoría o nodo"""
        pass

class GeneroSimple(ComponenteGenero):
    """Hoja (Leaf) - Un género individual sin subcategorías"""
    def contiene(self, genero_buscar: str) -> bool:
        # En lugar de "==", usamos "in" para buscar la palabra dentro del texto
        return self._normalizar(self.nombre) in self._normalizar(genero_buscar)

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
        # Comprueba si la categoría principal está en el texto
        if self._normalizar(self.nombre) in self._normalizar(nombre_genero):
            return True
        # Si no, busca recursivamente en todos sus subgéneros hijos
        for sub in self.subgeneros:
            if sub.contiene(nombre_genero):
                return True
        return False