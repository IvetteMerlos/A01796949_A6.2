# Sistema de Reservaciones de Hotel
### A01796949 — Actividad 6.2

## Descripción

Sistema de reservaciones desarrollado en Python que permite gestionar hoteles, clientes y reservaciones mediante archivos JSON como mecanismo de persistencia.

El sistema implementa tres clases principales:

- **Hotel** — Administra la información de hoteles, habitaciones disponibles y reservaciones activas.
- **Customer** — Gestiona los datos de los clientes registrados en el sistema.
- **Reservation** — Vincula a un cliente con un hotel, controlando la disponibilidad de habitaciones.

## Estructura del proyecto

```
A01796949_A6.2/
│
├── hotel.py                  # Clase Hotel con operaciones CRUD
├── customer.py               # Clase Customer con operaciones CRUD
├── reservation.py            # Clase Reservation con operaciones CRUD
├── test_reservation_system.py # Pruebas unitarias con unittest
├── pylint_report.txt         # Reporte de calidad de código (10/10)
└── htmlcov/                  # Reporte de cobertura de pruebas (98%)
```

## Funcionalidades

### Hotel
- Crear, eliminar, mostrar y modificar hoteles
- Reservar y cancelar habitaciones

### Customer
- Crear, eliminar, mostrar y modificar clientes

### Reservation
- Crear una reservación vinculando cliente y hotel
- Cancelar una reservación existente

## Persistencia

Cada clase almacena su información en archivos JSON:
- `hotels.json`
- `customers.json`
- `reservations.json`

Los errores en los archivos son manejados e impresos en consola sin detener la ejecución del programa.

## Pruebas unitarias

El proyecto incluye 48 casos de prueba usando el módulo `unittest`, con casos positivos y negativos para cada clase.

