import sqlite3
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Back, Style, init
import csv
import subprocess
import sys
import os

"""
Gestor de Tareas

Desarrollado por: Ing. Billy Porras Meléndez
Día de Creación: 15 de Octubre de 2024

Descripción:
Este script implementa un gestor de tareas que permite a los usuarios agregar, listar y exportar tareas. 
Cada tarea incluye un nombre, la fecha de realización y las horas trabajadas. 

Características:
- Agregar nuevas tareas con el nombre de la tarea y el tiempo trabajado.
- Listar las tareas filtradas por una fecha específica.
- Exportar las tareas realizadas en un rango de fechas a un archivo CSV.
- Manejo de bases de datos SQLite para almacenar las tareas.
- Interfaz interactiva y colorida usando `tabulate` y `colorama` para mejorar la experiencia del usuario.

Este gestor de tareas está diseñado para ser intuitivo y eficiente en la gestión del tiempo trabajado en diferentes actividades diarias.

Librerías utilizadas:
- sqlite3: Manejo de la base de datos.
- datetime: Manejo de fechas y horas.
- tabulate: Presentación de datos en tablas con formato.
- colorama: Colorear la salida del terminal para mejorar la experiencia del usuario.
- csv: Exportar datos a archivos CSV.

"""

# Inicializa Colorama
init(autoreset=True)

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('tareas.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY,
    fecha TEXT,
    nombre_tarea TEXT,
    horas_trabajadas TEXT
)
''')

# Ruta del archivo de configuración
config_file_path = 'config.gestion'

# Configurar horas laborales por defecto
horas_laborales = "07:15"
horas_laborales_td = timedelta(hours=7, minutes=15)

def cargar_horas_laborales():
    global horas_laborales, horas_laborales_td
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            horas_laborales = file.readline().strip()
            horas_laborales_td = validar_horas(horas_laborales) or timedelta(hours=7, minutes=15)
    else:
        horas_laborales = "07:15"
        horas_laborales_td = timedelta(hours=7, minutes=15)

def guardar_horas_laborales():
    with open(config_file_path, 'w') as file:
        file.write(horas_laborales)

def mostrar_menu():
    print(Fore.BLUE + Style.BRIGHT + "==== Menú de Tareas ====")
    print(Fore.CYAN + Style.BRIGHT + "1."+ Fore.WHITE +" Agregar Tarea")
    print(Fore.CYAN + Style.BRIGHT + "2."+ Fore.WHITE +" Modificar Tarea")
    print(Fore.CYAN + Style.BRIGHT + "3."+ Fore.WHITE +" Listar Tareas (un día)")
    print(Fore.CYAN + Style.BRIGHT + "4."+ Fore.WHITE +" Listar Tareas (rango de fechas)")
    print(Fore.CYAN + Style.BRIGHT + "5."+ Fore.WHITE +" Eliminar Tarea")
    print(Fore.CYAN + Style.BRIGHT + "6."+ Fore.WHITE +" Establecer Horas Laborales")
    print(Fore.CYAN + Style.BRIGHT + "7."+ Fore.WHITE +" Exportar a CSV")
    print(Fore.CYAN + Style.BRIGHT + "8."+ Fore.WHITE +" Actualizar Librerías")
    print(Fore.RED + Style.BRIGHT + "9."+ Fore.WHITE +" Salir")
    print(Fore.BLUE + Style.BRIGHT + "10."+ Fore.WHITE +" Acerca de")
    print(Style.RESET_ALL)
    
def acerca_de():
    print(Fore.GREEN + "\n**************************************************")
    print(Fore.GREEN + "\nAcerca de:")
    print(Fore.BLUE + Style.BRIGHT + "\n__________________________________________________")
    print(Fore.BLUE + Style.BRIGHT + "\nDesarrollado por: Ing. Billy Porras Meléndez")
    print(Fore.BLUE + Style.BRIGHT + "Fecha de Creación: 15 de Octubre de 2024")
    print(Fore.BLUE + Style.BRIGHT + "Versión: 1.1.5")
    print(Fore.BLUE + Style.BRIGHT + "\n__________________________________________________")
    print(Fore.CYAN + "Este proyecto fue desarrollado con el objetivo de")
    print(Fore.CYAN + "proporcionar una herramienta simple, eficiente y")
    print(Fore.CYAN + "altamente personalizable para la gestión del tiempo")
    print(Fore.CYAN + "de trabajo diario. Con funcionalidades que permiten")
    print(Fore.CYAN + "el registro, la modificación y la exportación de")
    print(Fore.CYAN + "tareas, el gestor de tareas es ideal para aquellos")
    print(Fore.CYAN + "que buscan mantener un control preciso sobre sus")
    print(Fore.CYAN + "actividades diarias.")
    


    print(Fore.CYAN + "\nEste gestor de tareas está diseñado para ser")
    print(Fore.CYAN + "intuitivo, con colores y tablas bien organizadas")
    print(Fore.CYAN + "para mejorar la experiencia del usuario.")
    
    print(Fore.CYAN + "Desarrollado usando SQLite para almacenamiento")
    print(Fore.CYAN + "de datos y Tabulate para presentar la información")
    print(Fore.CYAN + "de manera estructurada.")
    print(Fore.GREEN + "\n**************************************************")

def validar_horas(horas):
    try:
        h, m = map(int, horas.split(':'))
        if h < 0 or m < 0 or m >= 60:
            raise ValueError
        return timedelta(hours=h, minutes=m)
    except Exception:
        print(Fore.RED + "Formato de horas inválido. Asegúrese de usar HH:MM.")
        return None

def calcular_horas_restantes(horas_trabajadas):
    cursor.execute('SELECT horas_trabajadas FROM tareas WHERE fecha = ?', (datetime.now().date(),))
    tareas = cursor.fetchall()
    
    tiempo_total_trabajado = sum([validar_horas(t[0]).total_seconds() for t in tareas], 0)
    tiempo_trabajado = validar_horas(horas_trabajadas)
    if tiempo_trabajado is None:
        return None
    tiempo_total_trabajado += tiempo_trabajado.total_seconds()
    
    tiempo_restante = horas_laborales_td - timedelta(seconds=tiempo_total_trabajado)
    return tiempo_restante

def obtener_fecha():
    fecha_input = input(Fore.GREEN + "Ingrese la fecha (DD/MM/YYYY) o presione Enter para hoy: ")
    if fecha_input:
        try:
            return datetime.strptime(fecha_input, "%d/%m/%Y").date()
        except ValueError:
            print(Fore.RED + "Fecha inválida. Se usará la fecha actual.")
    return datetime.now().date()

def obtener_rango_fechas():
    fecha_inicio = input(Fore.GREEN + "Ingrese la fecha de inicio (DD/MM/YYYY): ")
    fecha_fin = input(Fore.GREEN + "Ingrese la fecha de fin (DD/MM/YYYY): ")
    
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
        if fecha_fin_dt < fecha_inicio_dt:
            raise ValueError
        return fecha_inicio_dt, fecha_fin_dt
    except ValueError:
        print(Fore.RED + "Fechas inválidas o rango incorrecto.")
        return None, None

def agregar_tarea():
    while True:
        nombre_tarea = input(Fore.GREEN + "Ingrese el nombre de la tarea: ").strip()
        if nombre_tarea:
            break
        print(Fore.RED + "El nombre de la tarea no puede estar vacío.")
    
    horas_trabajadas = input(Fore.GREEN + "Ingrese las horas trabajadas (HH:MM): ")

    horas_restantes = calcular_horas_restantes(horas_trabajadas)
    if horas_restantes is None:
        return

    fecha = obtener_fecha()

    cursor.execute('INSERT INTO tareas (fecha, nombre_tarea, horas_trabajadas) VALUES (?, ?, ?)', 
                   (fecha, nombre_tarea, horas_trabajadas))
    conn.commit()

    print(Fore.YELLOW + f"Tarea '{nombre_tarea}' agregada. Tiempo restante del día: {horas_restantes}.")
    listar_tareas(fecha)
    print(Style.RESET_ALL)

def modificar_tarea():
    listar_tareas()
    try:
        tarea_id = int(input(Fore.GREEN + "Ingrese el ID de la tarea a modificar: "))

        # Obtener los valores actuales de la tarea
        cursor.execute('SELECT nombre_tarea, horas_trabajadas FROM tareas WHERE id = ?', (tarea_id,))
        tarea = cursor.fetchone()

        if tarea:
            nombre_actual, horas_actuales = tarea

            # Pedir nuevo nombre de tarea, con el valor actual por defecto
            nuevo_nombre = input(Fore.GREEN + f"Ingrese el nuevo nombre de la tarea (Enter para mantener '{nombre_actual}'): ")
            if not nuevo_nombre:
                nuevo_nombre = nombre_actual

            # Pedir nuevas horas trabajadas, con el valor actual por defecto
            nuevas_horas = input(Fore.GREEN + f"Ingrese las nuevas horas trabajadas (HH:MM) (Enter para mantener '{horas_actuales}'): ")
            if not nuevas_horas:
                nuevas_horas = horas_actuales
            else:
                if validar_horas(nuevas_horas) is None:
                    print(Fore.RED + "Formato de horas inválido.")
                    return

            # Actualizar la tarea
            cursor.execute('UPDATE tareas SET nombre_tarea = ?, horas_trabajadas = ? WHERE id = ?', 
                           (nuevo_nombre, nuevas_horas, tarea_id))
            conn.commit()
            print(Fore.YELLOW + "Tarea modificada con éxito.")
        else:
            print(Fore.RED + "Tarea no encontrada.")

    except Exception as e:
        print(Fore.RED + f"Error al modificar la tarea: {e}")

def eliminar_tarea():
    listar_tareas()
    try:
        tarea_id = int(input(Fore.GREEN + "Ingrese el ID de la tarea a eliminar: "))
        cursor.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
        conn.commit()
        print(Fore.YELLOW + "Tarea eliminada con éxito.")
    except Exception:
        print(Fore.RED + "Error al eliminar la tarea. Asegúrese de que el ID sea correcto.")

def listar_tareas(fecha=None):
    if fecha is None:
        fecha = obtener_fecha()

    cursor.execute('SELECT * FROM tareas WHERE fecha = ?', (fecha,))
    tareas = cursor.fetchall()

    if tareas:
        # Formatear el ID con color y preparar los datos para tabulate
        formatted_tareas = [
            [f"{Fore.CYAN}{tarea[0]}{Style.RESET_ALL}", tarea[1], tarea[2], tarea[3]]
            for tarea in tareas
        ]
        
        print(tabulate(formatted_tareas, headers=["ID", "Fecha", "Tarea", "Tiempo Laborado"], tablefmt="fancy_grid",maxcolwidths=[None, 30,30]))

        horas_totales = sum([validar_horas(tarea[3]).total_seconds() for tarea in tareas])
        tiempo_restante = horas_laborales_td - timedelta(seconds=horas_totales)
        print(Fore.YELLOW + Back.RED + Style.BRIGHT + f"Horas restantes del día {fecha}: {str(tiempo_restante).split('.')[0]}.Total de horas trabajadas {str(timedelta(seconds=horas_totales)).split('.')[0]}")
    else:
        print(Fore.YELLOW + "No hay tareas para el día especificado.")
    print(Style.RESET_ALL)

def listar_tareas_rango_fechas():
    fecha_inicio, fecha_fin = obtener_rango_fechas()
    if fecha_inicio and fecha_fin:
        cursor.execute('SELECT * FROM tareas WHERE fecha BETWEEN ? AND ?', (fecha_inicio, fecha_fin))
        tareas = cursor.fetchall()

        if tareas:
            # Formatear el ID con color y preparar los datos para tabulate
            formatted_tareas = [
                [f"{Fore.CYAN}{tarea[0]}{Style.RESET_ALL}", tarea[1], tarea[2], tarea[3]]
                for tarea in tareas
            ]
            
            print(tabulate(formatted_tareas, headers=["ID", "Fecha", "Tarea", "Tiempo Laborado"], tablefmt="fancy_grid",maxcolwidths=[None, 30,30]))

            horas_totales = sum([validar_horas(tarea[3]).total_seconds() for tarea in tareas])
            print(Fore.YELLOW + Back.RED + Style.BRIGHT + f"Horas totales trabajadas en el rango: {str(timedelta(seconds=horas_totales)).split('.')[0]}.")
        else:
            print(Fore.YELLOW + "No hay tareas para el rango de fechas especificado.")
    print(Style.RESET_ALL)

def exportar_a_csv():
    with open('tareas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Fecha", "Tarea", "Tiempo Laborado"])

        cursor.execute('SELECT * FROM tareas')
        tareas = cursor.fetchall()

        for tarea in tareas:
            writer.writerow(tarea)

    print(Fore.YELLOW + "Tareas exportadas a tareas.csv con éxito.")
    print(Style.RESET_ALL)

def establecer_horas_laborales():
    global horas_laborales, horas_laborales_td
    nuevo_horas = input(Fore.GREEN + "Ingrese las nuevas horas laborales (HH:MM): ")
    if validar_horas(nuevo_horas):
        horas_laborales = nuevo_horas
        horas_laborales_td = validar_horas(nuevo_horas)
        guardar_horas_laborales()
        print(Fore.YELLOW + "Horas laborales actualizadas con éxito.")
    else:
        print(Fore.RED + "Formato de horas inválido.")

def actualizar_librerias():
    # Este comando dependerá del sistema operativo, se asume que es un entorno basado en UNIX
    os.system("pip install --upgrade tabulate colorama")

# Cargar horas laborales al inicio
cargar_horas_laborales()

# Bucle principal
while True:
    mostrar_menu()
    opcion = input(Fore.GREEN + "Seleccione una opción: ")

    if opcion == '1':
        agregar_tarea()
    elif opcion == '2':
        modificar_tarea()
    elif opcion == '3':
        listar_tareas()
    elif opcion == '4':
        listar_tareas_rango_fechas()
    elif opcion == '5':
        eliminar_tarea()
    elif opcion == '6':
        establecer_horas_laborales()
    elif opcion == '7':
        exportar_a_csv()
    elif opcion == '8':
        actualizar_librerias()
    elif opcion == '9':
        print(Fore.YELLOW + "Saliendo del programa...")
        break
    elif opcion == '10':
        acerca_de()
    else:
        print(Fore.RED + "Opción inválida. Intente nuevamente.")

# Cerrar la conexión
conn.close()
