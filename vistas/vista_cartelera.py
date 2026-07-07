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

    def actualizar_filtros_dinamicos(self, peliculas):
        """Analiza las películas cargadas y añade categorías dinámicas estructuradas"""
        for p in peliculas:
            gen_str = p.get('genero', '')
            if not gen_str:
                continue

            partes = [g.strip() for g in gen_str.split(',')]
            cat_principal = partes[0]
            subgeneros = partes[1:] 

            nodo_padre = None
            for sub in self.raiz_generos.subgeneros:
                if sub.nombre.lower() == cat_principal.lower():
                    nodo_padre = sub
                    break

            if not nodo_padre:
                nodo_padre = CategoriaGenero(cat_principal)
                self.raiz_generos.agregar(nodo_padre)

            if isinstance(nodo_padre, CategoriaGenero):
                for sub_nombre in subgeneros:
                    existe_sub = any(hijo.nombre.lower() == sub_nombre.lower() for hijo in nodo_padre.subgeneros)
                    if not existe_sub:
                        nodo_padre.agregar(GeneroSimple(sub_nombre))
                
        opciones_principales = ["Todos"] + [sub.nombre for sub in self.raiz_generos.subgeneros]
        self.cb_genero.configure(values=opciones_principales)
        
        if self.cb_genero.get() not in opciones_principales:
            self.cb_genero.set("Todos")
            self.cb_subgenero.configure(values=["-"], state="disabled")
            self.cb_subgenero.set("-")

    def al_cambiar_genero(self, seleccion):
        if seleccion == "Todos":
            self.cb_subgenero.configure(values=["-"], state="disabled")
            self.cb_subgenero.set("-")
        else:
            categoria_actual = None
            for sub in self.raiz_generos.subgeneros:
                if sub.nombre == seleccion:
                    categoria_actual = sub
                    break
            
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

                # Frame contenedor para organizar la imagen a la izquierda y texto a la derecha
                frame_contenido = ctk.CTkFrame(frame_peli, fg_color="transparent")
                frame_contenido.pack(fill="both", expand=True, padx=15, pady=10)
                
                # --- RENDERIZADO DE LA IMAGEN ---
                ruta_imagen = pelicula.get("imagen", "")
                if ruta_imagen and os.path.exists(ruta_imagen):
                    try:
                        from PIL import Image
                        img_pil = Image.open(ruta_imagen)
                        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(120, 180))
                        lbl_img = ctk.CTkLabel(frame_contenido, image=img_ctk, text="")
                        lbl_img.pack(side="left", padx=(0, 15))
                    except Exception as e:
                        print(f"Error al cargar la imagen: {e}")
                
                # Frame lateral para agrupar toda la información
                frame_info = ctk.CTkFrame(frame_contenido, fg_color="transparent")
                frame_info.pack(side="left", fill="both", expand=True)

                titulo = pelicula.get('titulo', 'Sin Título')
                clasificacion = pelicula.get('clasificacion', 'N/A')
                duracion = pelicula.get('duracion', '-- min')

                info_texto = f"{titulo} | {duracion} | {clasificacion} | Género: {genero_peli}"
                lbl_info = ctk.CTkLabel(frame_info, text=info_texto, font=("Arial", 16, "bold"))
                lbl_info.pack(anchor="w", pady=(0, 5))

                lbl_sinopsis = ctk.CTkLabel(frame_info, text=pelicula.get('sinopsis', 'Sin sinopsis disponible.'), wraplength=400, justify="left")
                lbl_sinopsis.pack(anchor="w", pady=5)

                estado_guardado = pelicula.get('estado', 'En Cartelera')
                peli_modelo = Pelicula(
                    titulo=titulo,
                    duracion_minutos=duracion,
                    clasificacion=clasificacion,
                    estado_str=estado_guardado
                )

                if peli_modelo.intentar_reserva():
                    btn_reservar = ctk.CTkButton(frame_info, text="Ver y Reservar", 
                                                command=lambda p=pelicula: self.controlador.mostrar_reserva(p))
                    btn_reservar.pack(anchor="e", pady=(5, 0))
                else:
                    lbl_estado_msg = ctk.CTkLabel(frame_info, text=peli_modelo._estado.obtener_mensaje(), 
                                                font=("Arial", 13, "italic"), text_color="gray")
                    lbl_estado_msg.pack(anchor="e", pady=(5, 0))

        except json.JSONDecodeError:
            ctk.CTkLabel(self.contenedor_peliculas, text="Error: El formato de peliculas.json no es válido.", text_color="red").pack(pady=20)

    def cargar_peliculas(self):
        """Carga las películas aplicando los filtros y dibujándolas en formato cuadrícula (Grid)"""
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

            # 1. Separar las películas filtradas en dos listas
            peliculas_cartelera = []
            peliculas_proximamente = []

            for pelicula in peliculas:
                genero_peli = pelicula.get('genero', 'Desconocido')
                estado_peli = pelicula.get('estado', 'En Cartelera')
                
                if estado_peli == "Archivada":
                    continue

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

                if cumple_filtro:
                    if estado_peli == "En Cartelera":
                        peliculas_cartelera.append(pelicula)
                    elif estado_peli == "Próximamente":
                        peliculas_proximamente.append(pelicula)

            # --- CONFIGURACIÓN DE LA CUADRÍCULA ---
            max_columnas = 2 
            fila_actual = 0
            
            # Configuramos las columnas del contenedor para que se expandan equitativamente
            self.contenedor_peliculas.grid_columnconfigure(0, weight=1)
            self.contenedor_peliculas.grid_columnconfigure(1, weight=1)

            # 2. Función interna para dibujar cada película como una "Tarjeta" (Card) vertical
            def dibujar_pelicula(pelicula_datos, fila, columna):
                # Frame principal de la tarjeta
                frame_tarjeta = ctk.CTkFrame(self.contenedor_peliculas, corner_radius=10, width=260)
                frame_tarjeta.grid(row=fila, column=columna, pady=15, padx=15, sticky="nsew")
                
                # --- IMAGEN (CENTRAL Y ARRIBA) ---
                ruta_imagen = pelicula_datos.get("imagen", "")
                if ruta_imagen and os.path.exists(ruta_imagen):
                    try:
                        from PIL import Image
                        img_pil = Image.open(ruta_imagen)
                        # Hacemos el póster un poco más grande para este formato
                        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(160, 240))
                        lbl_img = ctk.CTkLabel(frame_tarjeta, image=img_ctk, text="")
                        lbl_img.pack(pady=(15, 10))
                    except Exception as e:
                        print(f"Error al cargar la imagen: {e}")
                else:
                    # Un cuadro por defecto si el administrador olvidó poner imagen
                    ctk.CTkLabel(frame_tarjeta, text="🎬\nSin Póster", font=("Arial", 18), width=160, height=240, fg_color="#2a2a2a", corner_radius=10).pack(pady=(15, 10))

                # --- INFO (ABAJO DE LA IMAGEN) ---
                titulo = pelicula_datos.get('titulo', 'Sin Título')
                if len(titulo) > 23: titulo = titulo[:20] + "..." # Acortamos si es muy largo
                
                ctk.CTkLabel(frame_tarjeta, text=titulo, font=("Arial", 16, "bold")).pack(pady=(0, 5))

                clasificacion = pelicula_datos.get('clasificacion', 'N/A')
                duracion = pelicula_datos.get('duracion', '-- min')
                genero = pelicula_datos.get('genero', 'Desconocido')
                
                detalles = f"⏳ {duracion}  |  🎬 {clasificacion}"
                ctk.CTkLabel(frame_tarjeta, text=detalles, font=("Arial", 12), text_color="gray").pack()
                ctk.CTkLabel(frame_tarjeta, text=genero, font=("Arial", 12, "italic"), text_color="#2daae1").pack(pady=(0, 15))

                # --- BOTÓN DE ESTADO / RESERVA ---
                estado_guardado = pelicula_datos.get('estado', 'En Cartelera')
                peli_modelo = Pelicula(
                    titulo=titulo,
                    duracion_minutos=duracion,
                    clasificacion=clasificacion,
                    estado_str=estado_guardado
                )

                if peli_modelo.intentar_reserva():
                    btn_reservar = ctk.CTkButton(frame_tarjeta, text="Comprar Entradas", fg_color="#1f538d", hover_color="#14375d", 
                                                command=lambda p=pelicula_datos: self.controlador.mostrar_reserva(p))
                    btn_reservar.pack(pady=(0, 15), padx=20, fill="x")
                else:
                    lbl_estado_msg = ctk.CTkLabel(frame_tarjeta, text=peli_modelo._estado.obtener_mensaje(), 
                                                font=("Arial", 13, "bold"), text_color="#d48806")
                    lbl_estado_msg.pack(pady=(0, 15))


            # 3. Dibujar la sección EN CARTELERA
            if peliculas_cartelera:
                ctk.CTkLabel(self.contenedor_peliculas, text="🎬 EN CARTELERA", font=("Arial", 20, "bold"), text_color="#2daae1").grid(row=fila_actual, column=0, columnspan=max_columnas, sticky="w", padx=20, pady=(20, 10))
                fila_actual += 1
                
                col_actual = 0
                for peli in peliculas_cartelera:
                    dibujar_pelicula(peli, fila_actual, col_actual)
                    col_actual += 1
                    if col_actual >= max_columnas:
                        col_actual = 0
                        fila_actual += 1
                
                if col_actual != 0: 
                    fila_actual += 1 

            # Separador visual
            if peliculas_cartelera and peliculas_proximamente:
                separador = ctk.CTkFrame(self.contenedor_peliculas, height=2, fg_color="#3b3b3b")
                separador.grid(row=fila_actual, column=0, columnspan=max_columnas, sticky="ew", padx=40, pady=20)
                fila_actual += 1

            # 4. Dibujar la sección PRÓXIMAMENTE
            if peliculas_proximamente:
                ctk.CTkLabel(self.contenedor_peliculas, text="🔜 PRÓXIMAMENTE", font=("Arial", 20, "bold"), text_color="#d48806").grid(row=fila_actual, column=0, columnspan=max_columnas, sticky="w", padx=20, pady=(10, 10))
                fila_actual += 1
                
                col_actual = 0
                for peli in peliculas_proximamente:
                    dibujar_pelicula(peli, fila_actual, col_actual)
                    col_actual += 1
                    if col_actual >= max_columnas:
                        col_actual = 0
                        fila_actual += 1

            # 5. Si no hay películas para los filtros
            if not peliculas_cartelera and not peliculas_proximamente:
                ctk.CTkLabel(self.contenedor_peliculas, text="No hay películas que coincidan con estos filtros.", font=("Arial", 14, "italic"), text_color="gray").grid(row=fila_actual, column=0, columnspan=max_columnas, pady=40)

        except json.JSONDecodeError:
            ctk.CTkLabel(self.contenedor_peliculas, text="Error: El formato de peliculas.json no es válido.", text_color="red").grid(row=0, column=0, pady=20)