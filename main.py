import customtkinter as ctk
import json
import os
from tkinter import messagebox

from vistas.vista_login import VistaLogin
from vistas.vista_cartelera import VistaCartelera
from vistas.vista_reserva import VistaReserva
from vistas.vista_mis_reservas import VistaMisReservas
from vistas.vista_admin import VistaAdmin 

class AppCine(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Cine")
        self.geometry("850x650")
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.usuario_actual = None 
        self.crear_archivos_base() 

        self.vista_login = VistaLogin(self, controlador=self)
        self.vista_cartelera = VistaCartelera(self, controlador=self)
        self.vista_reserva = VistaReserva(self, controlador=self)
        self.vista_mis_reservas = VistaMisReservas(self, controlador=self)
        self.vista_admin = VistaAdmin(self, controlador=self) 
        
        self.mostrar_login()

    def ocultar_todo(self):
        self.vista_login.pack_forget()
        self.vista_cartelera.pack_forget()
        self.vista_reserva.pack_forget()
        self.vista_mis_reservas.pack_forget()
        self.vista_admin.pack_forget()

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
                    reservas_usuario = [r for r in todas if r.get('cliente_correo') == self.usuario_actual['correo']]
            except json.JSONDecodeError:
                pass 
                
        self.vista_mis_reservas.cargar_mis_reservas(reservas_usuario)
        self.vista_mis_reservas.pack(fill="both", expand=True)

    def mostrar_admin(self): 
        self.ocultar_todo()
        self.vista_admin.pack(fill="both", expand=True)

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
        if correo.lower() == "admin" and password == "admin1234":
            self.mostrar_admin()
            return

        ruta = os.path.join("datos", "clientes.json")
        with open(ruta, "r", encoding="utf-8") as f:
            clientes = json.load(f)
            
        for c in clientes:
            if c["correo"] == correo and c["password"] == password:
                self.usuario_actual = c 
                self.mostrar_cartelera()
                return
                
        messagebox.showerror("Error", "Credenciales incorrectas.")

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.mostrar_login()

    def registrar_reserva(self, datos_reserva):
        datos_reserva["cliente_correo"] = self.usuario_actual["correo"]
        datos_reserva["cliente_nombre"] = self.usuario_actual["nombre"]

        ruta_reservas = os.path.join("datos", "reservas.json")
        reservas = []
        if os.path.exists(ruta_reservas):
            with open(ruta_reservas, "r", encoding="utf-8") as f:
                try:
                    reservas = json.load(f)
                except json.JSONDecodeError:
                    reservas = []
        
        reservas.append(datos_reserva)
        
        with open(ruta_reservas, "w", encoding="utf-8") as f:
            json.dump(reservas, f, indent=4)

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
                for funcion in peli.get("funciones", []):
                    if funcion.get("fecha") == datos_reserva["fecha"]:
                        for horario in funcion.get("horarios", []):
                            if horario.get("hora") == datos_reserva["hora"]:
                                if "idioma" in horario:
                                    if horario.get("idioma") == datos_reserva["idioma"]:
                                        ocupados = horario.get("asientos_ocupados", [])
                                        ocupados.extend(datos_reserva["asientos"])
                                        horario["asientos_ocupados"] = list(set(ocupados))
                                        break
                                elif "idiomas" in horario:
                                    idioma_elegido = datos_reserva.get("idioma", "Doblada")
                                    idiomas = horario.get("idiomas", {"Doblada": [], "Subtitulada": []})
                                    ocupados = idiomas.get(idioma_elegido, [])
                                    ocupados.extend(datos_reserva["asientos"])
                                    idiomas[idioma_elegido] = list(set(ocupados))
                                    horario["idiomas"] = idiomas
                                    break
                        break
                break
                
        with open(ruta_peliculas, "w", encoding="utf-8") as f:
            json.dump(peliculas, f, indent=4)

    def devolver_reserva(self, reserva_a_eliminar):
        ruta_reservas = os.path.join("datos", "reservas.json")
        if os.path.exists(ruta_reservas):
            with open(ruta_reservas, "r", encoding="utf-8") as f:
                reservas = json.load(f)
            
            reservas = [r for r in reservas if r != reserva_a_eliminar]
            
            with open(ruta_reservas, "w", encoding="utf-8") as f:
                json.dump(reservas, f, indent=4)

        ruta_peliculas = os.path.join("datos", "peliculas.json")
        if os.path.exists(ruta_peliculas):
            with open(ruta_peliculas, "r", encoding="utf-8") as f:
                peliculas = json.load(f)

            for peli in peliculas:
                if peli.get("titulo") == reserva_a_eliminar["pelicula_titulo"]:
                    for funcion in peli.get("funciones", []):
                        if funcion.get("fecha") == reserva_a_eliminar["fecha"]:
                            for horario in funcion.get("horarios", []):
                                if horario.get("hora") == reserva_a_eliminar["hora"]:
                                    idioma_reserva = reserva_a_eliminar.get("idioma", "Doblada")
                                    liberados = reserva_a_eliminar["asientos"]
                                    
                                    if "idioma" in horario:
                                        if horario.get("idioma") == idioma_reserva:
                                            ocupados = horario.get("asientos_ocupados", [])
                                            horario["asientos_ocupados"] = [a for a in ocupados if a not in liberados]
                                            break
                                    elif "idiomas" in horario:
                                        idiomas = horario.get("idiomas", {"Doblada": [], "Subtitulada": []})
                                        ocupados = idiomas.get(idioma_reserva, [])
                                        idiomas[idioma_reserva] = [a for a in ocupados if a not in liberados]
                                        horario["idiomas"] = idiomas
                                        break
                            break
                    break

            with open(ruta_peliculas, "w", encoding="utf-8") as f:
                json.dump(peliculas, f, indent=4)

        self.mostrar_mis_reservas()
        
    def crear_archivos_base(self):
        if not os.path.exists("datos"): os.makedirs("datos")
        # --- AÑADIMOS SALAS.JSON A LA CREACIÓN BASE ---
        archivos = ["clientes.json", "reservas.json", "peliculas.json", "salas.json"]
        for arc in archivos:
            ruta = os.path.join("datos", arc)
            if not os.path.exists(ruta):
                with open(ruta, "w", encoding="utf-8") as f:
                    if arc == "salas.json":
                        # Inyectamos una sala inicial por defecto para evitar listas vacías
                        json.dump([{"id": 1, "nombre": "Sala 1", "capacidad": 30, "tipo": "2D"}], f, indent=4)
                    else:
                        json.dump([], f)

if __name__ == "__main__":
    app = AppCine()
    app.mainloop()