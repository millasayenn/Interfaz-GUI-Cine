import json
import os

class GestorJSON:
    @staticmethod
    def leer_datos(ruta_archivo: str) -> list:
        # Si el archivo no existe, devuelve una lista vacía para evitar errores
        if not os.path.exists(ruta_archivo):
            return []
            
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)

    @staticmethod
    def guardar_datos(ruta_archivo: str, datos: list) -> bool:
        # Guarda los datos con indentación de 4 espacios para que sea legible por humanos
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True