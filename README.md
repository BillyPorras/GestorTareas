# Gestor de Tareas con SQLite
## Ing. Billy Porras Meléndez
Este programa permite gestionar tareas diarias utilizando una base de datos SQLite. Puedes agregar, modificar, listar y eliminar tareas, así como establecer horas laborales y exportar la información a un archivo CSV.

## Requisitos

Antes de ejecutar el programa, asegúrate de tener instalado Python 3.x en tu sistema. También necesitas las siguientes librerías:

- `sqlite3`: Incluida con Python.
- `tabulate`: Para mostrar la información de manera tabulada.
- `colorama`: Para añadir color a la salida del programa.

## Instalación de Librerías

Para instalar las librerías necesarias, abre una terminal y ejecuta el siguiente comando:

```bash
pip install tabulate colorama
```

## Actualización de Librerías

El programa también incluye una opción para actualizar automáticamente las librerías. Puedes hacer esto seleccionando la opción correspondiente en el menú del programa.

## Base de Datos

El programa utiliza una base de datos SQLite llamada `tareas.db`. Al iniciar el programa por primera vez, se creará automáticamente si no existe. La base de datos contiene una tabla llamada `tareas` con los siguientes campos:

- **id**: Identificador único de la tarea (entero).
- **fecha**: Fecha de la tarea (texto en formato YYYY-MM-DD).
- **nombre_tarea**: Nombre de la tarea (texto).
- **horas_trabajadas**: Horas trabajadas en la tarea (texto en formato HH:MM).

## Ejecución del Programa

Para ejecutar el programa, sigue estos pasos:

1. Clona este repositorio o descarga el archivo `gestor_tareas.py` en tu máquina local.

2. Abre una terminal y navega hasta el directorio donde se encuentra el archivo `gestor_tareas.py`.

3. Ejecuta el programa con el siguiente comando:

   ```bash
   python gestor_tareas.py

