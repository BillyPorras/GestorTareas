# Tutorial: Sistema de Gestión de Tareas en Python

Este tutorial te guiará sobre cómo usar el sistema de gestión de tareas en Python, el cual permite registrar tareas, calcular horas trabajadas, modificar tareas, y exportarlas a un archivo CSV, entre otras funcionalidades. A continuación, te mostramos cómo usar el sistema paso a paso.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Descripción del Sistema](#descripción-del-sistema)
- [Menú Principal](#menú-principal)
- [Funciones Disponibles](#funciones-disponibles)
  - [Agregar Tarea](#1-agregar-tarea)
  - [Modificar Tarea](#2-modificar-tarea)
  - [Listar Tareas (un día)](#3-listar-tareas-un-día)
  - [Listar Tareas (rango de fechas)](#4-listar-tareas-rango-de-fechas)
  - [Eliminar Tarea](#5-eliminar-tarea)
  - [Establecer Horas Laborales](#6-establecer-horas-laborales)
  - [Exportar a CSV](#7-exportar-a-csv)
  - [Actualizar Librerías](#8-actualizar-librerías)
  - [Salir del Sistema](#9-salir-del-sistema)
- [Conclusión](#conclusión)

---

## Requisitos

Antes de usar el sistema, asegúrate de tener instaladas las siguientes librerías de Python:

- `sqlite3` (incluido en la instalación estándar de Python)
- `tabulate`
- `colorama`

Puedes instalar las librerías necesarias ejecutando el siguiente comando:
```bash
  pip install tabulate colorama
```
## Instalación

1. Clona o descarga el código fuente del sistema.
2. Guarda el script en tu computadora.
3. Abre una terminal en la carpeta donde guardaste el archivo.
4. Ejecuta el script usando el comando:

```bash
python gestion_tareas.py
```
## Descripción del Sistema

El sistema permite gestionar tareas diarias, calcular horas trabajadas, modificar tareas previas, listar tareas realizadas y exportar esta información a un archivo CSV. La interfaz de usuario es interactiva, y te permite navegar por un menú para realizar las distintas acciones.

## Menú Principal

El menú principal presenta varias opciones que te permiten interactuar con el sistema. Cada opción está numerada, y para seleccionar una opción, simplemente introduce el número correspondiente y presiona `Enter`.

Las opciones disponibles en el menú son:

1. Agregar Tarea
2. Modificar Tarea
3. Listar Tareas (un día)
4. Listar Tareas (rango de fechas)
5. Eliminar Tarea
6. Establecer Horas Laborales
7. Exportar a CSV
8. Actualizar Librerías
9. Salir del Sistema

## Funciones Disponibles

### 1. Agregar Tarea

Esta opción te permite agregar una nueva tarea para el día actual o para una fecha específica. El sistema te solicitará el nombre de la tarea y el tiempo trabajado en formato `HH:MM`. Después de ingresar los datos, la tarea se almacenará en la base de datos.
```plain
Ingrese el nombre de la tarea: Revisión de informes
Ingrese las horas trabajadas (HH:MM): 02:30
```
### 2. Modificar Tarea

Permite modificar una tarea existente. Si no deseas cambiar algún campo (por ejemplo, el nombre de la tarea), puedes presionar `Enter` para mantener el valor actual.
```plain
Ingrese el ID de la tarea a modificar: 1
Ingrese el nuevo nombre de la tarea (Enter para mantener 'Revisión de informes'): 
Ingrese las nuevas horas trabajadas (HH:MM) (Enter para mantener '02:30'): 
```
### 3. Listar Tareas (un día)

Puedes listar las tareas realizadas en un día específico, ingresando la fecha en el formato `DD/MM/YYYY`. Si no introduces una fecha, el sistema utilizará la fecha actual.
```plain
Ingrese la fecha (DD/MM/YYYY) o presione Enter para hoy: 05/10/2024
```
### 4. Listar Tareas (rango de fechas)

Muestra todas las tareas realizadas dentro de un rango de fechas. Debes ingresar la fecha inicial y la fecha final en formato `DD/MM/YYYY`.
```plain
Ingrese la fecha de inicio (DD/MM/YYYY): 01/10/2024
Ingrese la fecha de fin (DD/MM/YYYY): 05/10/2024
```
### 5. Eliminar Tarea

Esta opción te permite eliminar una tarea específica. El sistema te solicitará que confirmes la eliminación.

```plain
Ingrese el ID de la tarea a eliminar: 2
```

### 6. Establecer Horas Laborales

Te permite configurar el número de horas laborales diarias. El sistema utiliza un valor predeterminado de `07:15` (7 horas y 15 minutos), pero puedes cambiarlo a tus necesidades.
```plain
Ingrese las horas laborales del día (HH:MM): 08:00
```

### 7. Exportar a CSV

Esta opción te permite exportar las tareas a un archivo CSV. El sistema solicitará la fecha o el rango de fechas de las tareas que deseas exportar.
```plain
Ingrese la fecha de inicio (DD/MM/YYYY): 01/10/2024
Ingrese la fecha de fin (DD/MM/YYYY): 05/10/2024
```
### 8. Actualizar Librerías

Si alguna librería necesita ser actualizada, el sistema ejecutará los comandos necesarios para instalar las últimas versiones.

### 9. Salir del Sistema

Esta opción finaliza la ejecución del sistema.

## Conclusión

Este sistema es una herramienta útil para gestionar tareas y llevar un registro de las horas trabajadas de manera diaria. Puedes personalizar las horas laborales, modificar o eliminar tareas, y exportar tus registros a un archivo CSV para un análisis posterior.
