# 🎬 Sistema de Reserva de Cine - Proyecto TPA

Este proyecto es una aplicación de escritorio desarrollada en Python enfocada en la gestión y reserva de asientos para un cine.

El diseño del sistema está estructurado utilizando la arquitectura **MVC (Modelo-Vista-Controlador)** y aplica estrictamente los principios **S.O.L.I.D.**, asegurando un código altamente cohesionado, con bajo acoplamiento y fácil de mantener.

## Próximas funciones a implementar:
* Modificación y eliminación de perfiles de usuario.
* Perfil de administrador.
    * Crear, modificar y eliminar películas.
    * Crear, modificar y eliminar funciones.
* Agregar más validaciones e inserar modulo 11 para RUT.

## Arquitectura y Diseño (UML)

Para resolver la instanciación de los métodos de pago sin acoplar el controlador a implementaciones concretas, se implementó el patrón creacional **Factory Method** (`FabricaPago`). Además, se utiliza el patrón **Strategy** para la ejecución de los cobros mediante la interfaz `IMetodoPago`.

A continuación se detalla el diagrama de clases del sistema, que incluye el flujo completo (CRUD) de las reservas:
```mermaid
classDiagram
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
    class VistaMisReservas {
        +cargar_mis_reservas(reservas: List)
        +solicitar_devolucion(reserva: Dict)
    }

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

    class IMetodoPago {
        <<interface>>
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
    class PagoTarjeta {
        +procesar_pago(monto: Float) Boolean
    }
    class PagoEfectivo {
        +procesar_pago(monto: Float) Boolean
    }

    AppCine *-- VistaLogin : Instancia y controla
    AppCine *-- VistaCartelera : Instancia y controla
    AppCine *-- VistaReserva : Instancia y controla
    AppCine *-- VistaMisReservas : Instancia y controla

    VistaReserva ..> FabricaPago : Solicita instanciación
    VistaReserva --> ProcesadorPago : Delega proceso de pago
    
    IMetodoPago <|.. PagoTarjeta : Implementa
    IMetodoPago <|.. PagoEfectivo : Implementa
    ProcesadorPago o-- IMetodoPago : Depende de (Composición)
    FabricaPago ..> IMetodoPago : Crea
    ```