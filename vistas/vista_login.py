import re
from tkinter import messagebox
import customtkinter as ctk

class VistaLogin(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        
        self.label_titulo = ctk.CTkLabel(self, text="Bienvenido al Cine", font=("Arial", 28, "bold"))
        self.label_titulo.pack(pady=(40, 20))

        self.tabview = ctk.CTkTabview(self, width=400, height=300)
        self.tabview.pack(pady=10, padx=20)
        
        self.tabview.add("Iniciar Sesión")
        self.tabview.add("Registrarse")

        # --- Iniciar Sesión ---
        self.entry_login_correo = ctk.CTkEntry(self.tabview.tab("Iniciar Sesión"), placeholder_text="Correo Electrónico", width=250)
        self.entry_login_correo.pack(pady=(30, 10))
        
        self.entry_login_pass = ctk.CTkEntry(self.tabview.tab("Iniciar Sesión"), placeholder_text="Contraseña", show="*", width=250)
        self.entry_login_pass.pack(pady=10)
        
        self.btn_login = ctk.CTkButton(self.tabview.tab("Iniciar Sesión"), text="Ingresar", command=self.intentar_login)
        self.btn_login.pack(pady=20)

        # --- Registrarse ---
        self.entry_reg_nombre = ctk.CTkEntry(self.tabview.tab("Registrarse"), placeholder_text="Nombre Completo", width=250)
        self.entry_reg_nombre.pack(pady=(20, 10))

        self.entry_reg_correo = ctk.CTkEntry(self.tabview.tab("Registrarse"), placeholder_text="Correo Electrónico", width=250)
        self.entry_reg_correo.pack(pady=10)

        self.entry_reg_pass = ctk.CTkEntry(self.tabview.tab("Registrarse"), placeholder_text="Contraseña", show="*", width=250)
        self.entry_reg_pass.pack(pady=10)

        self.btn_registrar = ctk.CTkButton(self.tabview.tab("Registrarse"), text="Crear Cuenta", fg_color="green", hover_color="darkgreen", command=self.intentar_registro)
        self.btn_registrar.pack(pady=20)

    # Método para validar el formato del correo
    def validar_correo(self, correo):
        import re
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(patron, correo))

    def intentar_login(self):
        correo = self.entry_login_correo.get()
        password = self.entry_login_pass.get()
        
        if not correo or not password:
            messagebox.showwarning("Error", "Complete todos los campos.")
            return
            
        if " " in correo or " " in password:
            messagebox.showwarning("Error", "El correo y la contraseña no pueden contener espacios en blanco.")
            return
            
        if not self.validar_correo(correo):
            messagebox.showwarning("Error", "El formato del correo es inválido (ej: usuario@correo.com).")
            return
            
        self.controlador.procesar_login(correo, password)

    def intentar_registro(self):
        nombre = self.entry_reg_nombre.get().strip() # El nombre sí puede llevar espacios
        correo = self.entry_reg_correo.get()
        password = self.entry_reg_pass.get()
        
        if not nombre or not correo or not password:
            messagebox.showwarning("Error", "Complete todos los campos.")
            return
            
        if " " in correo or " " in password:
            messagebox.showwarning("Error", "El correo y la contraseña no pueden contener espacios en blanco.")
            return
            
        if len(password) < 8:
            messagebox.showwarning("Error", "La contraseña debe tener un mínimo de 8 caracteres.")
            return
            
        if not self.validar_correo(correo):
            messagebox.showwarning("Error", "El formato del correo es inválido (ej: usuario@correo.com).")
            return
            
        self.controlador.procesar_registro(nombre, correo, password)

    def validar_correo(self, correo):
        # El correo debe terminar en gmail.com o outlook.com (y agregamos outlook.es por precaución)
        patron = r'^[\w\.-]+@(gmail\.com|outlook\.com|outlook\.es)$'
        return bool(re.match(patron, correo, re.IGNORECASE))

    def validar_nombre(self, nombre):
        # Permite solo letras mayúsculas, minúsculas, vocales con tilde, la letra ñ y espacios
        patron = r'^[A-Za-zÁ-Úá-úñÑ\s]+$'
        return bool(re.match(patron, nombre))

    def intentar_login(self):
        correo = self.entry_login_correo.get().strip()
        password = self.entry_login_pass.get()
        
        if not correo or not password:
            messagebox.showwarning("Error", "Complete todos los campos.")
            return
            
        if " " in correo or " " in password:
            messagebox.showwarning("Error", "El correo y la contraseña no pueden contener espacios en blanco.")
            return
            
        if not self.validar_correo(correo):
            messagebox.showwarning("Error", "El correo debe ser de dominio @gmail.com o @outlook.com.")
            return
            
        self.controlador.procesar_login(correo, password)

    def intentar_registro(self):
        nombre = self.entry_reg_nombre.get().strip() 
        correo = self.entry_reg_correo.get().strip()
        password = self.entry_reg_pass.get()
        
        if not nombre or not correo or not password:
            messagebox.showwarning("Error", "Complete todos los campos.")
            return
            
        # Validación: Sin números ni caracteres especiales en el nombre
        if not self.validar_nombre(nombre):
            messagebox.showwarning("Error", "El nombre de usuario solo debe contener letras, sin números ni caracteres especiales.")
            return
            
        if " " in correo or " " in password:
            messagebox.showwarning("Error", "El correo y la contraseña no pueden contener espacios en blanco.")
            return
            
        # Validación: Mínimo 8 caracteres en la contraseña
        if len(password) < 8:
            messagebox.showwarning("Error", "La contraseña debe tener un mínimo de 8 caracteres.")
            return
            
        # Validación: Gmail o Outlook exclusivamente
        if not self.validar_correo(correo):
            messagebox.showwarning("Error", "El correo debe ser de dominio @gmail.com o @outlook.com.")
            return
            
        self.controlador.procesar_registro(nombre, correo, password)