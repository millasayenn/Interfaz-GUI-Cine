#Uso la librería abc para crear la interfaz
from abc import ABC, abstractmethod

class IMetodoPago(ABC):
    @abstractmethod #Esto obliga a las clases hijas a usar este método
    def procesarCobro(self, monto: float) -> bool:
        pass #La interfaz define el nombre solamente, por eso usamos el metodo pass ya que las clases que hereden llenaran la funcion

"""Con la interfaz si trato de crear un objeto en
IMetodoPago directamente (ej: mipago= IMetodoPago()),}
me lanzará error ya que las interfaces no se
instancian, se implementan"""