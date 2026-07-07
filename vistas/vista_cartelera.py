import customtkinter as ctk
import json
import os
from modelos.genero import CategoriaGenero, GeneroSimple
from modelos.pelicula import Pelicula

class VistaCartelera(ctk.CTkFrame):
    def __init__(self, master, controlador, **kwargs):
        super().__init__(master, **kwargs)
        self.controlador = controlador
        self.pack_forget()

        # --- HEADER SUPERIOR ---
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(fill="x", padx=20, pady=10)

        self.lbl_bienvenida = ctk.CTkLabel(self.frame_header, text="Bienvenido", font=("Arial", 16, "bold"))
        self.lbl_bienvenida.pack(side="left")

        self.btn_logout = ctk.CTkButton(self.frame_header, text="Cerrar Sesión", fg_color="red", hover_color="darkred", width=100, command=self.controlador.cerrar_sesion)
        self.btn_logout.pack(side="right", padx=5)

        self.btn_mis_reservas = ctk.CTkButton(self.frame_header, text="Ver Mis Reservas", fg_color="#1f538d", width=120, command=self.controlador.mostrar_mis_reservas)
        self.btn_mis_reservas.pack(side="right", padx=5)

        self.label_titulo = ctk.CTkLabel(self, text="Cartelera de Cine", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

        # --- FILTROS DE GÉNERO Y SUBGÉNERO (PATRÓN COMPOSITE) ---
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=10, fill="x", padx=20)

        self.construir_arbol_generos()

        self.lbl_genero = ctk.CTkLabel(self.frame_filtros, text="Género:", font=("Arial", 13, "bold"))
        self.lbl_genero.pack(side="left", padx=5)
        
        opciones_principales = ["Todos"] + [sub.nombre for sub in self.raiz_generos.subgeneros]

        self.cb_genero = ctk.CTkComboBox(self.frame_filtros, values=opciones_principales, command=self.al_cambiar_genero, state="readonly")
        self.cb_genero.pack(side="left", padx=5)
        self.cb_genero.set("Todos")

        self.lbl_subgenero = ctk.CTkLabel(self.frame_filtros, text="Subgénero:", font=("Arial", 13, "bold"))
        self.lbl_subgenero.pack(side="left", padx=(20, 5))

        self.cb_subgenero = ctk.CTkComboBox(self.frame_filtros, values=["-"], command=self.al_cambiar_subgenero, width=200)
        self.cb_subgenero.pack(side="left", padx=5)
        self.cb_subgenero.configure(state="disabled")
        self.cb_subgenero.set("-")

        self.contenedor_peliculas = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.contenedor_peliculas.pack(pady=10, padx=20, fill="both", expand=True)

    def construir_arbol_generos(self):
        """Inicializa la estructura Composite jerárquica base estática"""
        self.raiz_generos = CategoriaGenero("Todos")
        # Ya no necesitamos quemar "Acción" aquí porque la función de abajo 
        # lo detectará y creará automáticamente desde el JSON.

    def actualizar_filtros_dinamicos(self, peliculas):
        """Analiza las películas cargadas y añade categorías dinámicas estructuradas"""
        for p in peliculas:
            gen_str = p.get('genero', '')
            if not gen_str:
                continue

            # Separamos el string por comas
            partes = [g.strip() for g in gen_str.split(',')]
            
            # La primera palabra es la Categoría Padre (Ej: "Familiar" o "Acción")
            cat_principal = partes[0]
            # Todo lo que esté después de la coma son Subgéneros (Ej: "Animación" o "Superhéroes")
            subgeneros = partes[1:] 

            # 1. Buscamos si la Categoría Principal ya existe en nuestro árbol
            nodo_padre = None
            for sub in self.raiz_generos.subgeneros:
                if sub.nombre.lower() == cat_principal.lower():
                    nodo_padre = sub
                    break

            # 2. Si no existe, la creamos y la añadimos a la raíz "Todos"
            if not nodo_padre:
                nodo_padre = CategoriaGenero(cat_principal)
                self.raiz_generos.agregar(nodo_padre)

            # 3. Añadimos los subgéneros específicos a su nodo padre
            if isinstance(nodo_padre, CategoriaGenero):
                for sub_nombre in subgeneros:
                    # Verificamos que el subgénero no esté repetido
                    existe_sub = any(hijo.nombre.lower() == sub_nombre.lower() for hijo in nodo_padre.subgeneros)
                    if not existe_sub:
                        nodo_padre.agregar(GeneroSimple(sub_nombre))
                
        # Actualizar silenciosamente el menú desplegable principal
        opciones_principales = ["Todos"] + [sub.nombre for sub in self.raiz_generos.subgeneros]
        self.cb_genero.configure(values=opciones_principales)
        
        # Seguridad: Si el usuario estaba filtrando algo que se borró, regresarlo a "Todos"
        if self.cb_genero.get() not in opciones_principales:
            self.cb_genero.set("Todos")
            self.cb_subgenero.configure(values=["-"], state="disabled")
            self.cb_subgenero.set("-")

    def al_cambiar_genero(self, seleccion):
        """Se ejecuta al cambiar el ComboBox principal. Despliega los subgéneros."""
        if seleccion == "Todos":
            self.cb_subgenero.configure(values=["-"], state="disabled")
            self.cb_subgenero.set("-")
        else:
            categoria_actual = None
            for sub in self.raiz_generos.subgeneros:
                if sub.nombre == seleccion:
                    categoria_actual = sub
                    break
            
            # Solo habilita el menú de subgéneros si la categoría padre realmente tiene hijos
            if categoria_actual and isinstance(categoria_actual, CategoriaGenero) and categoria_actual.subgeneros:
                opciones_sub = ["Todos (de esta categoría)"] + [hijo.nombre for hijo in categoria_actual.subgeneros]
                self.cb_subgenero.configure(values=opciones_sub, state="readonly")
                self.cb_subgenero.set("Todos (de esta categoría)")
            else:
                self.cb_subgenero.configure(values=["No tiene subgéneros"], state="disabled")
                self.cb_subgenero.set("No tiene subgéneros")
        
        self.cargar_peliculas()

    def al_cambiar_subgenero(self, seleccion):
        self.cargar_peliculas()

    def actualizar_bienvenida(self, nombre_usuario):
        self.lbl_bienvenida.configure(text=f"Hola, {nombre_usuario}")

    def cargar_peliculas(self):
        """Carga las películas aplicando los filtros jerárquicos del Composite"""
        for widget in self.contenedor_peliculas.winfo_children():
            widget.destroy()

        ruta_json = os.path.join("datos", "peliculas.json")
        if not os.path.exists(ruta_json):
            ctk.CTkLabel(self.contenedor_peliculas, text="Error: No se encontró el archivo peliculas.json").pack(pady=20)
            return

        try:
            with open(ruta_json, "r", encoding="utf-8") as archivo:
                peliculas = json.load(archivo)
                
            if not peliculas:
                ctk.CTkLabel(self.contenedor_peliculas, text="La cartelera está vacía en este momento.").pack(pady=20)
                return

            self.construir_arbol_generos()
            self.actualizar_filtros_dinamicos(peliculas)

            genero_principal = self.cb_genero.get()
            subgenero_elegido = self.cb_subgenero.get()

            for pelicula in peliculas:
                genero_peli = pelicula.get('genero', 'Desconocido')
                cumple_filtro = False
                
                if genero_principal == "Todos":
                    cumple_filtro = True
                else:
                    nodo_padre = None
                    for sub in self.raiz_generos.subgeneros:
                        if sub.nombre == genero_principal:
                            nodo_padre = sub
                            break
                    
                    if nodo_padre:
                        if subgenero_elegido in ["Todos (de esta categoría)", "-", "No tiene subgéneros"]:
                            cumple_filtro = nodo_padre.contiene(genero_peli)
                        else:
                            nodo_hijo = None
                            if isinstance(nodo_padre, CategoriaGenero):
                                for hijo in nodo_padre.subgeneros:
                                    if hijo.nombre == subgenero_elegido:
                                        nodo_hijo = hijo
                                        break
                            if nodo_hijo:
                                cumple_filtro = nodo_hijo.contiene(genero_peli)
                    else:
                        cumple_filtro = (genero_peli.lower() == genero_principal.lower())

                if not cumple_filtro:
                    continue 

                frame_peli = ctk.CTkFrame(self.contenedor_peliculas, corner_radius=10)
                frame_peli.pack(pady=10, padx=10, fill="x")

                titulo = pelicula.get('titulo', 'Sin Título')
                clasificacion = pelicula.get('clasificacion', 'N/A')
                duracion = pelicula.get('duracion', '-- min')

                info_texto = f"{titulo} | {duracion} | {clasificacion} | Género: {genero_peli}"
                lbl_info = ctk.CTkLabel(frame_peli, text=info_texto, font=("Arial", 16, "bold"))
                lbl_info.pack(anchor="w", padx=15, pady=(10, 5))

                lbl_sinopsis = ctk.CTkLabel(frame_peli, text=pelicula.get('sinopsis', 'Sin sinopsis disponible.'), wraplength=500, justify="left")
                lbl_sinopsis.pack(anchor="w", padx=15, pady=5)

                estado_guardado = pelicula.get('estado', 'En Cartelera')
                peli_modelo = Pelicula(
                    titulo=titulo,
                    duracion_minutos=duracion,
                    clasificacion=clasificacion,
                    estado_str=estado_guardado
                )

                if peli_modelo.intentar_reserva():
                    btn_reservar = ctk.CTkButton(frame_peli, text="Ver y Reservar", 
                                                command=lambda p=pelicula: self.controlador.mostrar_reserva(p))
                    btn_reservar.pack(anchor="e", padx=15, pady=(5, 10))
                else:
                    lbl_estado_msg = ctk.CTkLabel(frame_peli, text=peli_modelo._estado.obtener_mensaje(), 
                                                font=("Arial", 13, "italic"), text_color="gray")
                    lbl_estado_msg.pack(anchor="e", padx=15, pady=(5, 10))

        except json.JSONDecodeError:
            ctk.CTkLabel(self.contenedor_peliculas, text="Error: El formato de peliculas.json no es válido.", text_color="red").pack(pady=20)