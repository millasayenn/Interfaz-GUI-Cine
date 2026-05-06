class Cliente:
    """
    Clase que representa a un cliente del sistema de reservas de cine.
    """
    def __init__(self, id_cliente: int, nombre: str, email: str):
        self._id = id_cliente
        self._nombre = nombre
        self._email = email

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email