import customtkinter as ctk
import json
import os
from tkinter import messagebox

# Importamos las 4 vistas
from vistas.vista_login import VistaLogin
from vistas.vista_cartelera import VistaCartelera
from vistas.vista_reserva import VistaReserva
from vistas.vista_mis_reservas import VistaMisReservas

class AppCine(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Cine")
        self.geometry("850x650")
        
        # Variable de sesión
        self.usuario_actual = None 
        self.crear_archivos_base() # Asegura que existan los JSON

        # Instanciar vistas
        self.vista_login = VistaLogin(self, controlador=self)
        self.vista_cartelera = VistaCartelera(self, controlador=self)
        self.vista_reserva = VistaReserva(self, controlador=self)
        self.vista_mis_reservas = VistaMisReservas(self, controlador=self)
        
        # Iniciar mostrando el login
        self.mostrar_login()

    def ocultar_todo(self):
        self.vista_login.pack_forget()
        self.vista_cartelera.pack_forget()
        self.vista_reserva.pack_forget()
        self.vista_mis_reservas.pack_forget()

    # --- RUTAS / NAVEGACIÓN ---
    def mostrar_login(self):
        self.ocultar_todo()
        self.vista_login.pack(fill="both", expand=True)

    def mostrar_cartelera(self):
        self.ocultar_todo()
        self.vista_cartelera.actualizar_bienvenida(self.usuario_actual['nombre'])
        self.vista_cartelera.cargar_peliculas() 
        self.vista_cartelera.pack(fill="both", expand=True)

    def mostrar_reserva(self, pelicula):
        self.ocultar_todo()
        self.vista_reserva.actualizar_informacion(pelicula) 
        self.vista_reserva.pack(fill="both", expand=True)

    def mostrar_mis_reservas(self):
        self.ocultar_todo()
        
        ruta_reservas = os.path.join("datos", "reservas.json")
        reservas_usuario = []
        
        if os.path.exists(ruta_reservas):
            try:
                with open(ruta_reservas, "r", encoding="utf-8") as f:
                    todas = json.load(f)
                    # Filtramos solo las que coinciden con el correo del usuario actual
                    reservas_usuario = [r for r in todas if r.get('cliente_correo') == self.usuario_actual['correo']]
            except json.JSONDecodeError:
                pass # Si el archivo está vacío, la lista se queda vacía sin lanzar error
                
        self.vista_mis_reservas.cargar_mis_reservas(reservas_usuario)
        self.vista_mis_reservas.pack(fill="both", expand=True)

    # --- LÓGICA DE SESIÓN ---
    def procesar_registro(self, nombre, correo, password):
        ruta = os.path.join("datos", "clientes.json")
        with open(ruta, "r", encoding="utf-8") as f:
            clientes = json.load(f)
            
        if any(c["correo"] == correo for c in clientes):
            messagebox.showerror("Error", "Este correo ya está registrado.")
            return

        nuevo_cliente = {"nombre": nombre, "correo": correo, "password": password}
        clientes.append(nuevo_cliente)
        
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(clientes, f, indent=4)
            
        messagebox.showinfo("Éxito", "Registro completado. Ahora puede iniciar sesión.")

    def procesar_login(self, correo, password):
        ruta = os.path.join("datos", "clientes.json")
        with open(ruta, "r", encoding="utf-8") as f:
            clientes = json.load(f)
            
        for c in clientes:
            if c["correo"] == correo and c["password"] == password:
                self.usuario_actual = c # Guardamos los datos del usuario en sesión
                self.mostrar_cartelera()
                return
                
        messagebox.showerror("Error", "Credenciales incorrectas.")

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.mostrar_login()

    # --- LÓGICA DE RESERVA ---
    def registrar_reserva(self, datos_reserva):
        # Los datos se asignan automáticamente usando la sesión actual
        datos_reserva["cliente_correo"] = self.usuario_actual["correo"]
        datos_reserva["cliente_nombre"] = self.usuario_actual["nombre"]

        # 1. Guardar en reservas.json (Solución al JSONDecodeError)
        ruta_reservas = os.path.join("datos", "reservas.json")
        reservas = []
        if os.path.exists(ruta_reservas):
            with open(ruta_reservas, "r", encoding="utf-8") as f:
                try:
                    reservas = json.load(f)
                except json.JSONDecodeError:
                    reservas = [] # Si el archivo está vacío o corrupto, crea una lista
                    
        reservas.append(datos_reserva)
        
        with open(ruta_reservas, "w", encoding="utf-8") as f:
            json.dump(reservas, f, indent=4)

        # 2. Actualizar peliculas.json
        ruta_peliculas = os.path.join("datos", "peliculas.json")
        peliculas = []
        if os.path.exists(ruta_peliculas):
            with open(ruta_peliculas, "r", encoding="utf-8") as f:
                try:
                    peliculas = json.load(f)
                except json.JSONDecodeError:
                    peliculas = []

        for peli in peliculas:
            if peli.get("titulo") == datos_reserva["pelicula_titulo"]:
                ocupados = peli.get("asientos_ocupados", [])
                ocupados.extend(datos_reserva["asientos"]) 
                peli["asientos_ocupados"] = ocupados
                break
                
        with open(ruta_peliculas, "w", encoding="utf-8") as f:
            json.dump(peliculas, f, indent=4)

    # --- UTILIDAD ---
    def crear_archivos_base(self):
        """Asegura que los archivos JSON existan para evitar errores de lectura"""
        if not os.path.exists("datos"): os.makedirs("datos")
        archivos = ["clientes.json", "reservas.json", "peliculas.json"]
        for arc in archivos:
            ruta = os.path.join("datos", arc)
            if not os.path.exists(ruta):
                with open(ruta, "w", encoding="utf-8") as f:
                    json.dump([], f)

if __name__ == "__main__":
    app = AppCine()
    app.mainloop()