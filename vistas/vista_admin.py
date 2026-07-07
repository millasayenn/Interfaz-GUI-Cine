import customtkinter as ctk
import json
import os
import copy
from tkinter import messagebox

class VistaAdmin(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pack_forget()
        
        self.ruta_peliculas = os.path.join("datos", "peliculas.json")
        self.ruta_salas = os.path.join("datos", "salas.json")
        self.funciones_en_edicion = [] 
        
        self.crear_interfaz_principal()

    def crear_interfaz_principal(self):
        # Header global del administrador
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(fill="x", padx=20, pady=(15, 0))

        ctk.CTkLabel(self.frame_header, text="Panel de Administración", font=("Arial", 24, "bold")).pack(side="left")
        self.btn_logout = ctk.CTkButton(self.frame_header, text="Cerrar Sesión", fg_color="red", hover_color="darkred", width=100, command=self.controlador.cerrar_sesion)
        self.btn_logout.pack(side="right")

        # Sistema de pestañas para dividir Películas y Salas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tab_peliculas = self.tabview.add("Películas")
        self.tab_salas = self.tabview.add("Salas")

        self.crear_tab_peliculas()
        self.crear_tab_salas()

    # ==========================================
    #           MÓDULO DE PELÍCULAS
    # ==========================================
    def crear_tab_peliculas(self):
        btn_nueva = ctk.CTkButton(self.tab_peliculas, text="➕ Nueva Película", fg_color="green", hover_color="darkgreen", command=lambda: self.abrir_modal_pelicula())
        btn_nueva.pack(pady=10)

        self.lista_peliculas = ctk.CTkScrollableFrame(self.tab_peliculas)
        self.lista_peliculas.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_lista_peliculas()

    def cargar_lista_peliculas(self):
        for widget in self.lista_peliculas.winfo_children():
            widget.destroy()
        if not os.path.exists(self.ruta_peliculas): return
        
        with open(self.ruta_peliculas, "r", encoding="utf-8") as f:
            peliculas = json.load(f)
            
        for peli in peliculas:
            frame_item = ctk.CTkFrame(self.lista_peliculas, fg_color="#2b2b2b")
            frame_item.pack(fill="x", pady=5, padx=5)
            
            info = f"{peli.get('titulo')}  |  {peli.get('duracion')}  |  {peli.get('estado')}"
            ctk.CTkLabel(frame_item, text=info, font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=10)
            
            btn_del = ctk.CTkButton(frame_item, text="🗑 Eliminar", fg_color="red", hover_color="darkred", width=70, command=lambda p=peli: self.eliminar_pelicula(p))
            btn_del.pack(side="right", padx=10)
            
            btn_edit = ctk.CTkButton(frame_item, text="✎ Editar", fg_color="#d48806", hover_color="#b37305", width=70, command=lambda p=peli: self.abrir_modal_pelicula(p))
            btn_edit.pack(side="right", padx=5)

    def abrir_modal_pelicula(self, pelicula=None):
        modal_peli = ctk.CTkToplevel(self)
        modal_peli.title("Editar Película" if pelicula else "Nueva Película")
        # Hacemos la ventana más ancha para que quepan las dos columnas
        modal_peli.geometry("950x650")
        modal_peli.attributes("-topmost", True)
        modal_peli.grab_set()

        # Preparar datos
        es_edicion = pelicula is not None
        id_peli = pelicula.get("id", "") if es_edicion else ""
        
        # Migrador automático integrado para la edición
        if es_edicion:
            funciones_migradas = []
            for f in pelicula.get("funciones", []):
                fecha = f.get("fecha")
                horarios_nuevos = []
                for h in f.get("horarios", []):
                    if "idiomas" in h: 
                        for idioma_key, asientos in h["idiomas"].items():
                            horarios_nuevos.append({"hora": h.get("hora"), "idioma": idioma_key, "sala": "Sala 1 (2D)", "asientos_ocupados": asientos})
                    else: 
                        horarios_nuevos.append(h)
                funciones_migradas.append({"fecha": fecha, "horarios": horarios_nuevos})
            self.funciones_en_edicion = copy.deepcopy(funciones_migradas)
        else:
            self.funciones_en_edicion = []

        # ==========================================
        #       LAYOUT DE DOS COLUMNAS
        # ==========================================
        frame_main = ctk.CTkFrame(modal_peli, fg_color="transparent")
        frame_main.pack(fill="both", expand=True, padx=10, pady=10)

        # COLUMNA IZQUIERDA: Datos de la Película
        frame_izq = ctk.CTkFrame(frame_main, fg_color="transparent", width=400)
        frame_izq.pack(side="left", fill="both", expand=False, padx=10, pady=10)

        ctk.CTkLabel(frame_izq, text="Datos de la Película", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(frame_izq, text="Título:").pack(anchor="w", pady=(5,0))
        ent_titulo = ctk.CTkEntry(frame_izq, width=350)
        ent_titulo.pack(pady=(0,10))
        if es_edicion: ent_titulo.insert(0, pelicula.get("titulo", ""))

        ctk.CTkLabel(frame_izq, text="Duración (Ej: 1h 45m):").pack(anchor="w", pady=(5,0))
        ent_duracion = ctk.CTkEntry(frame_izq, width=350)
        ent_duracion.pack(pady=(0,10))
        if es_edicion: ent_duracion.insert(0, pelicula.get("duracion", ""))

        ctk.CTkLabel(frame_izq, text="Género (Ej: Acción, Aventura):").pack(anchor="w", pady=(5,0))
        ent_genero = ctk.CTkEntry(frame_izq, width=350)
        ent_genero.pack(pady=(0,10))
        if es_edicion: ent_genero.insert(0, pelicula.get("genero", ""))

        ctk.CTkLabel(frame_izq, text="Clasificación (Ej: TE+7):").pack(anchor="w", pady=(5,0))
        ent_clasificacion = ctk.CTkEntry(frame_izq, width=350)
        ent_clasificacion.pack(pady=(0,10))
        if es_edicion: ent_clasificacion.insert(0, pelicula.get("clasificacion", ""))

        ctk.CTkLabel(frame_izq, text="Estado:").pack(anchor="w", pady=(5,0))
        cb_estado = ctk.CTkComboBox(frame_izq, values=["En Cartelera", "Próximamente", "Archivada"], state="readonly", width=350)
        cb_estado.pack(pady=(0,10))
        cb_estado.set(pelicula.get("estado", "En Cartelera") if es_edicion else "En Cartelera")

        ctk.CTkLabel(frame_izq, text="Sinopsis:").pack(anchor="w", pady=(5,0))
        txt_sinopsis = ctk.CTkTextbox(frame_izq, height=100, width=350)
        txt_sinopsis.pack(pady=(0,15))
        if es_edicion: txt_sinopsis.insert("0.0", pelicula.get("sinopsis", ""))


        # COLUMNA DERECHA: Gestor de Horarios Integrado
        frame_der = ctk.CTkFrame(frame_main, fg_color="#1a1a1a")
        frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame_der, text="Gestión de Horarios y Salas", font=("Arial", 18, "bold")).pack(pady=10)

        frame_inputs = ctk.CTkFrame(frame_der, fg_color="transparent")
        frame_inputs.pack(pady=5)

        ctk.CTkLabel(frame_inputs, text="Fecha (DD-MM-YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ent_fecha = ctk.CTkEntry(frame_inputs, width=150, placeholder_text="Ej: 20-06-2026")
        ent_fecha.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_inputs, text="Hora (HH:MM):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ent_hora = ctk.CTkEntry(frame_inputs, width=150, placeholder_text="Ej: 15:00")
        ent_hora.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_inputs, text="Idioma:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        cb_idioma = ctk.CTkComboBox(frame_inputs, values=["Doblada", "Subtitulada", "Original"], width=150, state="readonly")
        cb_idioma.grid(row=2, column=1, padx=5, pady=5)
        cb_idioma.set("Doblada")

        # Lectura de salas
        salas_disp = []
        if os.path.exists(self.ruta_salas):
            try:
                with open(self.ruta_salas, "r", encoding="utf-8") as f:
                    lista_s = json.load(f)
                    salas_disp = [f"{s['nombre']} ({s['tipo']})" for s in lista_s]
            except Exception:
                pass
        if not salas_disp: salas_disp = ["Sala 1 (2D)"]

        ctk.CTkLabel(frame_inputs, text="Sala Asignada:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        cb_sala = ctk.CTkComboBox(frame_inputs, values=salas_disp, width=150, state="readonly")
        cb_sala.grid(row=3, column=1, padx=5, pady=5)
        cb_sala.set(salas_disp[0])

        btn_agregar_h = ctk.CTkButton(frame_inputs, text="➕ Añadir Horario", fg_color="#1f538d", hover_color="#14375d")
        btn_agregar_h.grid(row=4, column=0, columnspan=2, pady=10)

        frame_lista_h = ctk.CTkScrollableFrame(frame_der, width=400)
        frame_lista_h.pack(pady=5, padx=15, fill="both", expand=True)

        def refrescar_lista_h():
            for w in frame_lista_h.winfo_children(): w.destroy()
            if not self.funciones_en_edicion:
                ctk.CTkLabel(frame_lista_h, text="No hay funciones registradas.", text_color="gray").pack(pady=20)
                return

            for i, funcion in enumerate(self.funciones_en_edicion):
                fecha = funcion.get("fecha", "")
                ctk.CTkLabel(frame_lista_h, text=f"📅 {fecha}", font=("Arial", 13, "bold"), text_color="#2daae1").pack(anchor="w", pady=(5, 2), padx=5)
                for j, horario in enumerate(funcion.get("horarios", [])):
                    hora = horario.get("hora", "")
                    idioma = horario.get("idioma", "")
                    sala = horario.get("sala", "")
                    
                    frame_h = ctk.CTkFrame(frame_lista_h, fg_color="#3b3b3b")
                    frame_h.pack(fill="x", pady=2, padx=10)
                    texto_info = f"🕒 {hora} | {idioma} | {sala}"
                    ctk.CTkLabel(frame_h, text=texto_info).pack(side="left", padx=10, pady=5)
                    
                    btn_del = ctk.CTkButton(frame_h, text="X", width=30, height=25, fg_color="red", hover_color="darkred", command=lambda f_idx=i, h_idx=j: eliminar_horario(f_idx, h_idx))
                    btn_del.pack(side="right", padx=2, pady=5)
                    btn_edit = ctk.CTkButton(frame_h, text="✎", width=30, height=25, fg_color="#d48806", hover_color="#b37305", command=lambda f_idx=i, h_idx=j: editar_horario(f_idx, h_idx))
                    btn_edit.pack(side="right", padx=2, pady=5)

        def eliminar_horario(f_idx, h_idx):
            del self.funciones_en_edicion[f_idx]["horarios"][h_idx]
            if len(self.funciones_en_edicion[f_idx]["horarios"]) == 0:
                del self.funciones_en_edicion[f_idx]
            refrescar_lista_h()

        def editar_horario(f_idx, h_idx):
            fecha_editar = self.funciones_en_edicion[f_idx]["fecha"]
            horario_editar = self.funciones_en_edicion[f_idx]["horarios"][h_idx]
            ent_fecha.delete(0, "end"); ent_fecha.insert(0, fecha_editar)
            ent_hora.delete(0, "end"); ent_hora.insert(0, horario_editar["hora"])
            cb_idioma.set(horario_editar.get("idioma", "Doblada"))
            cb_sala.set(horario_editar.get("sala", salas_disp[0]))
            
            btn_agregar_h.configure(text="✅ Actualizar Horario", fg_color="#d48806", hover_color="#b37305")
            eliminar_horario(f_idx, h_idx)

        def guardar_nuevo_horario():
            fecha = ent_fecha.get().strip()
            hora = ent_hora.get().strip()
            idioma = cb_idioma.get()
            sala = cb_sala.get()
            
            if not fecha or not hora:
                messagebox.showwarning("Aviso", "Debes ingresar fecha y hora.", parent=modal_peli)
                return

            # Validación Interna
            for f in self.funciones_en_edicion:
                if f["fecha"] == fecha:
                    for h in f["horarios"]:
                        if h["hora"] == hora and h["sala"] == sala:
                            messagebox.showerror("Cruce de Salas", f"Ya asignaste la {sala} a las {hora} en esta misma película.", parent=modal_peli)
                            return
                        if h["hora"] == hora and h["idioma"] == idioma:
                            messagebox.showerror("Cruce de Idioma", f"Esta película ya tiene una función {idioma} a las {hora}.", parent=modal_peli)
                            return

            # Validación Global
            if os.path.exists(self.ruta_peliculas):
                with open(self.ruta_peliculas, "r", encoding="utf-8") as f_json:
                    todas_peliculas = json.load(f_json)
                for peli in todas_peliculas:
                    if str(peli.get("id", "")) == str(id_peli): continue 
                    for f in peli.get("funciones", []):
                        if f.get("fecha") == fecha:
                            for h in f.get("horarios", []):
                                if h.get("hora") == hora and h.get("sala", "Sala 1 (2D)") == sala:
                                    messagebox.showerror("Sala Ocupada", f"La {sala} ya está reservada para '{peli.get('titulo')}' a las {hora} el {fecha}.", parent=modal_peli)
                                    return

            funcion_obj = next((f for f in self.funciones_en_edicion if f["fecha"] == fecha), None)
            if not funcion_obj:
                funcion_obj = {"fecha": fecha, "horarios": []}
                self.funciones_en_edicion.append(funcion_obj)

            funcion_obj["horarios"].append({"hora": hora, "idioma": idioma, "sala": sala, "asientos_ocupados": []})
            ent_hora.delete(0, "end")
            btn_agregar_h.configure(text="➕ Añadir Horario", fg_color="#1f538d", hover_color="#14375d")
            refrescar_lista_h()

        btn_agregar_h.configure(command=guardar_nuevo_horario)
        refrescar_lista_h()

        # ==========================================
        #       BOTÓN GLOBAL DE GUARDADO
        # ==========================================
        def guardar_cambios():
            titulo = ent_titulo.get().strip()
            if not titulo:
                messagebox.showwarning("Error", "El título es obligatorio.", parent=modal_peli)
                return

            nueva_peli = {
                "titulo": titulo,
                "duracion": ent_duracion.get().strip(),
                "genero": ent_genero.get().strip(),
                "clasificacion": ent_clasificacion.get().strip(),
                "sinopsis": txt_sinopsis.get("0.0", "end").strip(),
                "estado": cb_estado.get(),
                "funciones": self.funciones_en_edicion 
            }

            with open(self.ruta_peliculas, "r", encoding="utf-8") as f: 
                peliculas = json.load(f)
            
            if es_edicion: 
                nueva_peli["id"] = int(id_peli)
                for i, p in enumerate(peliculas):
                    if p.get("id") == int(id_peli):
                        peliculas[i] = nueva_peli
                        break
            else: 
                nuevo_id = max([p.get("id", 0) for p in peliculas], default=0) + 1
                nueva_peli["id"] = nuevo_id
                peliculas.append(nueva_peli)

            with open(self.ruta_peliculas, "w", encoding="utf-8") as f: 
                json.dump(peliculas, f, indent=4, ensure_ascii=False)
            
            # --- ELIMINA O COMENTA ESTA LÍNEA ---
            # messagebox.showinfo("Éxito", "Película guardada correctamente.")
            
            self.cargar_lista_peliculas()
            modal_peli.destroy() # Esto cerrará la ventana automáticamente

        ctk.CTkButton(modal_peli, text="💾 Guardar Película Completa", fg_color="green", hover_color="darkgreen", height=45, font=("Arial", 16, "bold"), command=guardar_cambios).pack(fill="x", padx=20, pady=(0, 20))

    def eliminar_pelicula(self, pelicula):
        if messagebox.askyesno("Confirmar", f"¿Eliminar la película '{pelicula.get('titulo')}'?"):
            with open(self.ruta_peliculas, "r", encoding="utf-8") as f: 
                peliculas = json.load(f)
            peliculas = [p for p in peliculas if p.get("id") != pelicula.get("id")]
            with open(self.ruta_peliculas, "w", encoding="utf-8") as f: 
                json.dump(peliculas, f, indent=4, ensure_ascii=False)
            self.cargar_lista_peliculas()

    # ==========================================
    #             MÓDULO DE SALAS
    # ==========================================
    def crear_tab_salas(self):
        btn_nueva = ctk.CTkButton(self.tab_salas, text="➕ Nueva Sala", fg_color="green", hover_color="darkgreen", command=lambda: self.abrir_modal_sala())
        btn_nueva.pack(pady=10)

        self.lista_salas = ctk.CTkScrollableFrame(self.tab_salas)
        self.lista_salas.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_lista_salas()

    def cargar_lista_salas(self):
        for widget in self.lista_salas.winfo_children(): widget.destroy()
        if not os.path.exists(self.ruta_salas): return
        with open(self.ruta_salas, "r", encoding="utf-8") as f:
            salas = json.load(f)
        for s in salas:
            frame_item = ctk.CTkFrame(self.lista_salas, fg_color="#2b2b2b")
            frame_item.pack(fill="x", pady=5, padx=5)
            
            info = f"{s.get('nombre')}  |  Capacidad: {s.get('capacidad')}  |  {s.get('tipo')}"
            ctk.CTkLabel(frame_item, text=info, font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=10)
            
            btn_del = ctk.CTkButton(frame_item, text="🗑 Eliminar", fg_color="red", hover_color="darkred", width=70, command=lambda sal=s: self.eliminar_sala(sal))
            btn_del.pack(side="right", padx=10)
            
            btn_edit = ctk.CTkButton(frame_item, text="✎ Editar", fg_color="#d48806", hover_color="#b37305", width=70, command=lambda sal=s: self.abrir_modal_sala(sal))
            btn_edit.pack(side="right", padx=5)

    def abrir_modal_sala(self, sala=None):
        modal_sala = ctk.CTkToplevel(self)
        modal_sala.title("Editar Sala" if sala else "Nueva Sala")
        modal_sala.geometry("400x350")
        modal_sala.attributes("-topmost", True)
        modal_sala.grab_set()

        es_edicion = sala is not None
        id_sala = sala.get("id", "") if es_edicion else ""

        frame_form = ctk.CTkFrame(modal_sala, fg_color="transparent")
        frame_form.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame_form, text="Nombre de la Sala (Ej: Sala 1):").pack(anchor="w")
        ent_nombre = ctk.CTkEntry(frame_form, width=350)
        ent_nombre.pack(pady=(0,15))
        if es_edicion: ent_nombre.insert(0, sala.get("nombre", ""))

        ctk.CTkLabel(frame_form, text="Capacidad (Asientos):").pack(anchor="w")
        ent_capacidad = ctk.CTkEntry(frame_form, width=350)
        ent_capacidad.pack(pady=(0,15))
        if es_edicion: ent_capacidad.insert(0, str(sala.get("capacidad", "")))

        ctk.CTkLabel(frame_form, text="Tipo de Proyección:").pack(anchor="w")
        cb_tipo = ctk.CTkComboBox(frame_form, values=["2D", "3D", "IMAX", "4DX", "VIP"], state="readonly", width=350)
        cb_tipo.pack(pady=(0,20))
        cb_tipo.set(sala.get("tipo", "2D") if es_edicion else "2D")

        def guardar_cambios():
            nombre = ent_nombre.get().strip()
            capacidad = ent_capacidad.get().strip()
            if not nombre or not capacidad.isdigit():
                messagebox.showwarning("Error", "Nombre inválido o capacidad no es un número.", parent=modal_sala)
                return
            
            nueva_sala = {"nombre": nombre, "capacidad": int(capacidad), "tipo": cb_tipo.get()}
            with open(self.ruta_salas, "r", encoding="utf-8") as f: salas = json.load(f)
            
            if es_edicion:
                nueva_sala["id"] = int(id_sala)
                for i, s in enumerate(salas):
                    if s.get("id") == int(id_sala):
                        salas[i] = nueva_sala
                        break
            else:
                nuevo_id = max([s.get("id", 0) for s in salas], default=0) + 1
                nueva_sala["id"] = nuevo_id
                salas.append(nueva_sala)
                
            with open(self.ruta_salas, "w", encoding="utf-8") as f: json.dump(salas, f, indent=4, ensure_ascii=False)
            self.cargar_lista_salas()
            modal_sala.destroy()

        ctk.CTkButton(modal_sala, text="💾 Guardar Sala", fg_color="green", hover_color="darkgreen", height=40, font=("Arial", 14, "bold"), command=guardar_cambios).pack(fill="x", padx=20, pady=(0, 20))

    def eliminar_sala(self, sala):
        if messagebox.askyesno("Confirmar", f"¿Eliminar la sala '{sala.get('nombre')}'?"):
            with open(self.ruta_salas, "r", encoding="utf-8") as f: salas = json.load(f)
            salas = [s for s in salas if s.get("id") != sala.get("id")]
            with open(self.ruta_salas, "w", encoding="utf-8") as f: json.dump(salas, f, indent=4, ensure_ascii=False)
            self.cargar_lista_salas()