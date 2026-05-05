# 🎬 Sistema de Reserva de Cine - Proyecto TPA

Este proyecto es una aplicación de escritorio desarrollada en Python enfocada en la gestión y reserva de asientos para un cine.

El diseño del sistema está estructurado utilizando la arquitectura **MVC (Modelo-Vista-Controlador)** y aplica estrictamente los principios **S.O.L.I.D.**, asegurando un código altamente cohesionado, con bajo acoplamiento y fácil de mantener.

## Arquitectura y Diseño (UML)

Para resolver la instanciación de los métodos de pago sin acoplar el controlador a implementaciones concretas, se implementó el patrón creacional **Factory Method** (`FabricaPago`). Además, se utiliza el patrón **Strategy** para la ejecución de los cobros mediante la interfaz `IMetodoPago`.

A continuación se detalla el diagrama de clases del sistema, que incluye el flujo completo (CRUD) de las reservas:
```mermaid
classDiagram
    %% ==========================================
    %% CAPA DE VISTA (INTERFAZ DE USUARIO)
    %% ==========================================
    class VistaCartelera {
        +mostrarPeliculas(peliculas: List)
        +capturarSeleccionPelicula()
    }
    class VistaReserva {
        +mostrarMapaAsientos(asientos: List)
        +mostrarFormularioPago()
        +mostrarMensaje(mensaje: String)
    }

    %% ==========================================
    %% CAPA DE CONTROLADORES (ORQUESTADORES)
    %% ==========================================
    class ControladorReserva {
        -vista: VistaReserva
        -funcionActual: Funcion
        -procesadorPago: ProcesadorPago
        -notificador: INotificador
        +seleccionarAsiento(numero: String)
        +procesarCompra(tipoPago: String, cliente: Cliente)
        +modificarAsientoReserva(idReserva: Int, nuevoAsiento: String)
        +cancelarReserva(idReserva: Int)
    }

    %% ==========================================
    %% CAPA DE MODELOS (DOMINIO)
    %% ==========================================
    class Cliente {
        -id: Int
        -nombre: String
        -email: String
    }

    class Pelicula {
        -titulo: String
        -duracionMinutos: Int
        -clasificacion: String
    }

    class Sala {
        -numero: Int
        -capacidad: Int
    }

    class Funcion {
        -fechaHora: Datetime
        -pelicula: Pelicula
        -sala: Sala
        -asientos: List~Asiento~
        +obtenerAsientosDisponibles() List
        +marcarAsientoOcupado(numero: String)
        +liberarAsiento(numero: String)
    }

    class Asiento {
        -numero: String
        -ocupado: Boolean
        +estaOcupado() Boolean
    }

    class Reserva {
        -idReserva: Int
        -fechaCreacion: Date
        -montoTotal: Float
        -estado: String
        -cliente: Cliente
        -asientosReservados: List~Asiento~
        +generarComprobante() String
        +cambiarEstado(nuevoEstado: String)
    }

    %% ==========================================
    %% SERVICIOS, INTERFACES Y PATRONES CREACIONALES
    %% ==========================================
    class INotificador {
        <<interface>>
        +enviar(destinatario: String, mensaje: String)
    }

    class IMetodoPago {
        <<interface>>
        +procesarCobro(monto: Float) Boolean
    }
    
    class FabricaPago {
        <<Factory Method>>
        +crearMetodoPago(tipo: String) IMetodoPago
    }

    class ProcesadorPago {
        -estrategiaPago: IMetodoPago
        +setMetodoPago(metodo: IMetodoPago)
        +ejecutarPago(monto: Float) Boolean
    }

    class PagoTarjeta {
        +procesarCobro(monto: Float) Boolean
    }

    class PagoEfectivo {
        +procesarCobro(monto: Float) Boolean
    }

    %% ==========================================
    %% RELACIONES
    %% ==========================================
    
    VistaReserva <-- ControladorReserva : Actualiza
    ControladorReserva --> Funcion : Consulta/Modifica
    ControladorReserva --> ProcesadorPago : Usa
    ControladorReserva --> Reserva : Crea / Modifica
    ControladorReserva --> INotificador : Usa
    ControladorReserva ..> FabricaPago : Solicita instanciación

    Funcion "1" --> "1" Pelicula
    Funcion "1" --> "1" Sala
    Funcion "1" *-- "*" Asiento : Contiene
    Reserva "1" o-- "*" Asiento : Agrupa
    Reserva "1" --> "1" Cliente : Pertenece a

    IMetodoPago <|.. PagoTarjeta : Implementa
    IMetodoPago <|.. PagoEfectivo : Implementa
    ProcesadorPago o-- IMetodoPago : Depende de
    FabricaPago ..> IMetodoPago : Crea