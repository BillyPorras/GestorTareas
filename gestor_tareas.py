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
    print(Fore.CYAN + "3. Listar Tareas")
    print(Fore.CYAN + "4. Eliminar Tarea")
    print(Fore.CYAN + "5. Establecer Horas Laborales")
    print(Fore.CYAN + "6. Exportar a CSV")
    print(Fore.CYAN + "7. Actualizar Librerías")
    print(Fore.CYAN + "8. Salir")
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
    tiempo_trabajado = validar_horas(horas_trabajadas)
    if tiempo_trabajado is None:
        return None
    tiempo_restante = horas_laborales_td - tiempo_trabajado
    return tiempo_restante

def obtener_fecha():
    fecha_input = input(Fore.GREEN + "Ingrese la fecha (DD/MM/YYYY) o presione Enter para hoy: ")
    if fecha_input:
        try:
            return datetime.strptime(fecha_input, "%d/%m/%Y").date()
        except ValueError:
            print(Fore.RED + "Fecha inválida. Se usará la fecha actual.")
    return datetime.now().date()

def agregar_tarea():
    nombre_tarea = input(Fore.GREEN + "Ingrese el nombre de la tarea: ")
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
        nombre_tarea = input(Fore.GREEN + "Ingrese el nuevo nombre de la tarea: ")
        horas_trabajadas = input(Fore.GREEN + "Ingrese las nuevas horas trabajadas (HH:MM): ")
        
        cursor.execute('UPDATE tareas SET nombre_tarea = ?, horas_trabajadas = ? WHERE id = ?', 
                       (nombre_tarea, horas_trabajadas, tarea_id))
        conn.commit()
        print(Fore.YELLOW + "Tarea modificada con éxito.")
    except Exception:
        print(Fore.RED + "Error al modificar la tarea. Asegúrese de que el ID sea correcto.")

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
        print(tabulate(tareas, headers=["ID", "Fecha", "Nombre Tarea", "Horas Trabajadas"], tablefmt="pretty"))
        horas_totales = sum([validar_horas(tarea[3]).total_seconds() for tarea in tareas])
        tiempo_restante = horas_laborales_td - timedelta(seconds=horas_totales)
        print(Fore.YELLOW + f"Horas restantes del día: {str(tiempo_restante).split('.')[0]}.")
    else:
        print(Fore.YELLOW + "No hay tareas para el día especificado.")
    print(Style.RESET_ALL)

def exportar_a_csv():
    fecha = obtener_fecha()
    cursor.execute('SELECT * FROM tareas WHERE fecha = ?', (fecha,))
    tareas = cursor.fetchall()

    if tareas:
        with open(f'tareas_{fecha}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Fecha", "Nombre Tarea", "Horas Trabajadas"])
            writer.writerows(tareas)
        print(Fore.YELLOW + f"Tareas exportadas a tareas_{fecha}.csv con éxito.")
    else:
        print(Fore.RED + "No hay tareas para exportar.")
    print(Style.RESET_ALL)

def establecer_horas_laborales():
    global horas_laborales, horas_laborales_td
    horas_input = input(Fore.GREEN + "Ingrese las horas laborales (HH:MM) o presione Enter para usar el valor por defecto (07:15): ")
    if horas_input:
        horas_validas = validar_horas(horas_input)
        if horas_validas:
            horas_laborales = horas_input
            horas_laborales_td = horas_validas
            print(Fore.YELLOW + f"Horas laborales actualizadas a {horas_laborales}.")
        else:
            print(Fore.RED + "No se pudo actualizar las horas laborales debido a un formato inválido.")
    else:
        print(Fore.YELLOW + "Se mantendrán las horas laborales por defecto: 07:15.")

def actualizar_librerias():
    print(Fore.YELLOW + "Actualizando librerías...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "tabulate", "colorama"])
        print(Fore.GREEN + "Librerías actualizadas con éxito.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al actualizar las librerías: {e}")

def main():
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
            eliminar_tarea()
        elif opcion == '5':
            establecer_horas_laborales()
        elif opcion == '6':
            exportar_a_csv()
        elif opcion == '7':
            actualizar_librerias()
        elif opcion == '8':
            print(Fore.YELLOW + "Saliendo del programa.")
            break
        else:
            print(Fore.RED + "Opción no válida, intente de nuevo.")
    
    conn.close()

if __name__ == "__main__":
    main()
