import sqlite3
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Style, init
import csv
import subprocess
import sys

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

# Configurar horas laborales por defecto
horas_laborales = "07:15"
horas_laborales_td = timedelta(hours=7, minutes=15)

def mostrar_menu():
    print(Fore.BLUE + "==== Menú de Tareas ====")
    print(Fore.CYAN + "1. Agregar Tarea")
    print(Fore.CYAN + "2. Modificar Tarea")
    print(Fore.CYAN + "3. Listar Tareas (un día)")
    print(Fore.CYAN + "4. Listar Tareas (rango de fechas)")
    print(Fore.CYAN + "5. Eliminar Tarea")
    print(Fore.CYAN + "6. Establecer Horas Laborales")
    print(Fore.CYAN + "7. Exportar a CSV")
    print(Fore.CYAN + "8. Actualizar Librerías")
    print(Fore.CYAN + "9. Salir")
    print(Style.RESET_ALL)

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
            [f"{Fore.CYAN}{tarea[0]}{Style.RESET_ALL}", tarea[1], tarea[2]]
            for tarea in tareas
        ]
        
        print(tabulate(formatted_tareas, headers=["ID", "Nombre Tarea", "Horas Trabajadas"], tablefmt="pretty"))

        horas_totales = sum([validar_horas(tarea[3]).total_seconds() for tarea in tareas])
        tiempo_restante = horas_laborales_td - timedelta(seconds=horas_totales)
        print(Fore.YELLOW + f"Horas restantes del día: {str(tiempo_restante).split('.')[0]}.")
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
            [f"{Fore.CYAN}{tarea[0]}{Style.RESET_ALL}", tarea[1], tarea[2]]
            for tarea in tareas
        ]
        
        print(tabulate(formatted_tareas, headers=["ID", "Nombre Tarea", "Horas Trabajadas"], tablefmt="pretty"))

        horas_totales = sum([validar_horas(tarea[3]).total_seconds() for tarea in tareas])
        tiempo_restante = horas_laborales_td - timedelta(seconds=horas_totales)
        print(Fore.YELLOW + f"Horas restantes del día: {str(tiempo_restante).split('.')[0]}.")
    else:
        print(Fore.YELLOW + "No hay tareas para el día especificado.")
    print(Style.RESET_ALL)

def exportar_a_csv():
    fecha_inicio, fecha_fin = obtener_rango_fechas()
    if fecha_inicio and fecha_fin:
        cursor.execute('SELECT * FROM tareas WHERE fecha BETWEEN ? AND ?', (fecha_inicio, fecha_fin))
        tareas = cursor.fetchall()

        if tareas:
            with open(f'tareas_{fecha_inicio}_a_{fecha_fin}.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Fecha", "Nombre Tarea", "Horas Trabajadas"])
                writer.writerows(tareas)
            print(Fore.YELLOW + f"Tareas exportadas a tareas_{fecha_inicio}_a_{fecha_fin}.csv con éxito.")
        else:
            print(Fore.RED + "No hay tareas para exportar en el rango de fechas especificado.")
    else:
        print(Fore.RED + "No se exportaron tareas debido a fechas inválidas.")

def establecer_horas_laborales():
    global horas_laborales, horas_laborales_td
    horas_laborales = input(Fore.GREEN + "Ingrese las horas laborales del día (HH:MM): ")
    horas_laborales_td = validar_horas(horas_laborales)
    if horas_laborales_td is not None:
        print(Fore.YELLOW + f"Horas laborales establecidas: {horas_laborales}.")
    else:
        horas_laborales = "07:15"
        horas_laborales_td = timedelta(hours=7, minutes=15)

def actualizar_librerias():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "colorama", "tabulate"])
        print(Fore.GREEN + "Librerías actualizadas con éxito.")
    except Exception as e:
        print(Fore.RED + f"Error al actualizar las librerías: {e}")

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
    else:
        print(Fore.RED + "Opción no válida. Intente de nuevo.")
