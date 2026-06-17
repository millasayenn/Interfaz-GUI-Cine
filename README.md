# 🎬 Sistema de Reserva de Cine - Proyecto TPA

Este proyecto es una aplicación de escritorio desarrollada en Python enfocada en la gestión y reserva de asientos para un cine.

El diseño del sistema está estructurado utilizando la arquitectura **MVC (Modelo-Vista-Controlador)** y aplica estrictamente los principios **S.O.L.I.D.**, asegurando un código altamente cohesionado, con bajo acoplamiento y fácil de mantener.

## Próximas funciones a implementar:

* Estéticas:
    * Mostrar imágenes de cada película.
    * En mis reservas mostrar el precio final del adulto y niño y el precio total.
    * En mis reservas mostrar el idioma y genero de la película.
    * En mis reservas mostrar la sala en la que se encuentra la película. 

* Modificación y eliminación de perfiles de usuario.
* Vista para el perfil de administrador.
    * Crear, modificar y eliminar películas.
    * Crear, modificar y eliminar funciones.
* Mejorar validaciones:
    * Insertar módulo 11 para RUT de usuario.
    * Restricciones para devoluciones de asientos, por ejemplo, no poder devolver un asiento si quedan menos de 24 horas para la función.


## Arquitectura y Diseño (UML)

Para resolver la instanciación de los métodos de pago sin acoplar el controlador a implementaciones concretas, se implementó el patrón creacional **Factory Method** (`FabricaPago`). Además, se utiliza el patrón **Strategy** para la ejecución de los cobros mediante la interfaz `IMetodoPago`.

A continuación se detalla el diagrama de clases del sistema, que incluye el flujo completo (CRUD) de las reservas:
```mermaid
classDiagram
    %% --- CLASE PRINCIPAL Y VISTAS (MVC) ---
    class AppCine {
        -usuario_actual: Dict
        +mostrar_login()
        +mostrar_cartelera()
        +mostrar_reserva(pelicula: Dict)
        +mostrar_mis_reservas()
        +procesar_login(correo: String, password: String)
        +procesar_registro(nombre: String, correo: String, password: String)
        +registrar_reserva(datos_reserva: Dict)
        +devolver_reserva(reserva_a_eliminar: Dict)
    }

    class VistaMisReservas {
        +cargar_mis_reservas(reservas: List)
        +solicitar_devolucion(reserva: Dict)
    }

    class VistaLogin {
        +intentar_login()
        +intentar_registro()
    }

    class VistaCartelera {
        +actualizar_bienvenida(nombre: String)
        +cargar_peliculas()
    }

    class VistaReserva {
        -asientos_seleccionados: List
        +al_seleccionar_fecha()
        +al_seleccionar_hora()
        +iniciar_pago()
        +finalizar_reserva()
    }

    %% --- SISTEMA DE PAGOS (FACTORY METHOD & STRATEGY) ---
    class IMetodoPago {
        <<interface>>
        +procesar_pago(monto: Float) Boolean
    }

    class PagoTarjeta {
        +procesar_pago(monto: Float) Boolean
    }

    class PagoEfectivo {
        +procesar_pago(monto: Float) Boolean
    }

    class FabricaPago {
        <<Factory Method>>
        +crear_pago(tipo: String) IMetodoPago
    }

    class ProcesadorPago {
        -metodo_pago: IMetodoPago
        +procesar_pago(monto: Float) Boolean
    }

    %% --- SISTEMA DE GÉNEROS (PATRÓN COMPOSITE) ---
    class ComponenteGenero {
        <<interface>>
        +obtener_peliculas() List
        +obtener_nombre() String
    }

    class SubgeneroHoja {
        -nombre: String
        -peliculas: List
        +obtener_peliculas() List
        +obtener_nombre() String
    }

    class GeneroCompuesto {
        -nombre: String
        -subgeneros: List~ComponenteGenero~
        +agregar(g: ComponenteGenero)
        +obtener_peliculas() List
        +obtener_nombre() String
    }

    %% --- RELACIONES APP Y VISTAS ---
    AppCine *-- VistaMisReservas : Instancia y controla
    AppCine *-- VistaLogin : Instancia y controla
    AppCine *-- VistaCartelera : Instancia y controla
    AppCine *-- VistaReserva : Instancia y controla

    %% --- CONEXIÓN DE LA VISTA CON EL COMPOSITE ---
    VistaCartelera --> ComponenteGenero : Usa/Depende

    %% --- RELACIONES DEL PATRÓN COMPOSITE ---
    ComponenteGenero <|.. SubgeneroHoja : Implementa
    ComponenteGenero <|.. GeneroCompuesto : Implementa
    GeneroCompuesto o--> ComponenteGenero : Contiene (Agregación)

    %% --- RELACIONES DEL SISTEMA DE PAGOS ---
    VistaReserva ..> FabricaPago : Solicita instanciación
    VistaReserva --> ProcesadorPago : Delega proceso de pago

    FabricaPago ..> IMetodoPago : Crea
    ProcesadorPago o-- IMetodoPago : Depende de (Composición)
    
    IMetodoPago <|.. PagoTarjeta : Implementa
    IMetodoPago <|.. PagoEfectivo : Implementa
