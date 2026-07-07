# 🎬 Sistema de Gestión y Reserva de Cine (GUI)

Este proyecto es una aplicación de escritorio con Interfaz Gráfica de Usuario (GUI) desarrollada en Python (usando la librería CustomTkinter), diseñada para simular un sistema completo de un cine. Permite tanto la gestión administrativa de películas y horarios, como la experiencia del cliente para visualizar la cartelera, elegir asientos y simular la compra de entradas.

## Características Principales

### Vista de Administrador
* **Gestión de Películas:** Permite crear, editar y archivar películas, asignando títulos, duración, clasificación y subida de **Pósters/Imágenes** mediante un explorador de archivos.
* **Programación Dinámica:** Gestor de funciones que permite asignar múltiples fechas, horas e idiomas a cada película.
* **Control de Salas:** Asignación de salas dinámicas con validación de cruces de horarios para evitar que dos películas se proyecten en el mismo lugar y a la misma hora.

### Vista de Usuario (Cliente)
* **Cartelera Interactiva:** Presentación de películas en formato cuadrícula (Grid) separadas automáticamente por su estado (**En Cartelera** y **Próximamente**).
* **Filtros Inteligentes:** Búsqueda jerárquica de películas mediante categorías principales y subgéneros.
* **Reserva de Asientos Visual:** Cuadrícula de asientos generada dinámicamente según la capacidad real de la sala asignada (ej. Sala 1 de 50 asientos, Sala VIP de 30). Indicadores visuales para asientos libres (gris) y ocupados (rojo).
* **Pasarela de Pago:** Simulación de compra con cálculo automático de totales según cantidad de adultos y niños, seleccionando el método de pago (Tarjeta o Efectivo).
* **Historial de Reservas:** Sección "Mis Reservas" para que el usuario consulte los tickets adquiridos.

---

## Arquitectura y Patrones de Diseño

El sistema está diseñado bajo principios de Programación Orientada a Objetos (POO) y aplica tres patrones de diseño fundamentales para resolver problemas estructurales y de comportamiento:

### 1. Patrón *Factory Method* (Creacional)
Se utilizó para abstraer e instanciar los diferentes **métodos de pago**. La fábrica (`FabricaPago`) decide qué clase instanciar (`PagoTarjeta` o `PagoEfectivo`) basándose en la selección del usuario, permitiendo que en el futuro se agreguen nuevos métodos (ej. PayPal, Transferencia) sin modificar la lógica principal de la pasarela.

### 2. Patrón *Composite* (Estructural)
Implementado en el sistema de **filtros de cartelera**. Los géneros se tratan como una estructura de árbol, donde existen Categorías Principales (`CategoriaGenero`, el composite) que pueden contener tanto Subgéneros individuales (`GeneroSimple`, las hojas) como otras categorías. Esto permite que la interfaz filtre las películas tratando a subgéneros e hiper-géneros de manera uniforme.

### 3. Patrón *State* (De Comportamiento)
Utilizado para manejar el ciclo de vida de las películas en el cine. Una película cambia su comportamiento en la GUI dependiendo de si su estado interno es `EnCartelera`, `Proximamente` o `Archivada`. Por ejemplo, el estado *Próximamente* muestra un botón descriptivo, mientras que el estado *En Cartelera* habilita el botón de compra, eliminando largas sentencias condicionales (`if/else`).

---

## Diagrama UML de Clases (Patrones)

```mermaid
classDiagram
    %% Patrón Factory Method
    class IMetodoPago {
        <<interface>>
        +procesar_pago(monto)
    }
    class PagoTarjeta {
        +procesar_pago(monto)
    }
    class PagoEfectivo {
        +procesar_pago(monto)
    }
    class FabricaPago {
        +crear_pago(tipo) IMetodoPago
    }
    class ProcesadorPago {
        -metodo_pago: IMetodoPago
        +procesar_pago(monto)
    }
    IMetodoPago <|.. PagoTarjeta
    IMetodoPago <|.. PagoEfectivo
    FabricaPago ..> IMetodoPago : Instancia
    ProcesadorPago o-- IMetodoPago

    %% Patrón Composite
    class ComponenteGenero {
        <<interface>>
        +nombre: String
        +contiene(genero) boolean
    }
    class GeneroSimple {
        +contiene(genero) boolean
    }
    class CategoriaGenero {
        -subgeneros: List
        +agregar(componente)
        +eliminar(componente)
        +contiene(genero) boolean
    }
    ComponenteGenero <|.. GeneroSimple
    ComponenteGenero <|.. CategoriaGenero
    CategoriaGenero o-- ComponenteGenero

    %% Patrón State
    class EstadoPelicula {
        <<interface>>
        +intentar_reserva() boolean
        +obtener_mensaje() String
    }
    class EnCartelera {
        +intentar_reserva() boolean
        +obtener_mensaje() String
    }
    class Proximamente {
        +intentar_reserva() boolean
        +obtener_mensaje() String
    }
    class Archivada {
        +intentar_reserva() boolean
        +obtener_mensaje() String
    }
    class Pelicula {
        -estado: EstadoPelicula
        +cambiar_estado(estado)
        +intentar_reserva()
    }
    EstadoPelicula <|.. EnCartelera
    EstadoPelicula <|.. Proximamente
    EstadoPelicula <|.. Archivada
    Pelicula o-- EstadoPelicula