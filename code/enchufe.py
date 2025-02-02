from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, PLUGIP, PLUGKEY, PLUGVERS, USERNAME_TUYA, PASSWORD, DEVICE_ID

import logging
import keyboard
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
)
import tuyapower
from firebase_config import inicializar_firebase
import time

# Inicializar base de datos Firebase
db = inicializar_firebase()

# Conectar a la API de Tuya
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, AuthType.CUSTOM)
openapi.connect(USERNAME_TUYA, PASSWORD)
logging.basicConfig(level=logging.DEBUG)

# Variable de control de estado
flag = True

# Obtener datos del enchufe inteligente
on, w, mA, V, err = tuyapower.deviceInfo(DEVICE_ID, PLUGIP, PLUGKEY, PLUGVERS)


def estado():
    return flag

### FUNCIONALIDADES 
# Cambiar estado encendido/apagado
def toggle_state():
    global flag
    flag = not flag  # Alterna el estado del flag

    commands = {'commands': [{'code': 'switch_1', 'value': flag}]}
    openapi.post(f'/v1.0/iot-03/devices/{DEVICE_ID}/commands', commands)
    print(f"Estado del enchufe: {'Encendido' if flag else 'Apagado'}")
    


# Guardar dato actual en la base de datos
def guardar_datos_firebase(on, w, mA, V):
    coleccion = db.collection('consumo_energetico') #nombre de la coleccion (si no existe la crea)
    datos = {
        "estado": on,
        "consumo_w": w,
        "corriente_mA": mA,
        "voltaje_V": V,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
    }
    coleccion.add(datos)
    print(f"Datos guardados en Firebase: {datos}")


# Obtener datos de la bbdd por intervalos 
def obtener_datos_por_intervalo(fecha_inicio, fecha_fin):
    """
    Obtiene documentos de una colección en Firestore dentro de un intervalo de tiempo.
    """
    coleccion_ref = db.collection('consumo_energetico')
    #documentos = coleccion_ref.where("timestamp", ">=", "2025-01-24").where("timestamp", "<=", "2025-01-25").stream()
    # Filtrar datos (usando strings si el timestamp es una cadena)
    documentos = coleccion_ref.where("timestamp", ">=", fecha_inicio.strftime("%Y-%m-%d")) \
                               .where("timestamp", "<=", fecha_fin.strftime("%Y-%m-%d")).stream()
    print(documentos)
    datos = [doc.to_dict() for doc in documentos]
    print("DATOSSSS:",datos)
    return datos


# Obtener todos los datos de la base de datos
def obtener_todos_los_datos():
    """Obtiene todos los documentos de la colección consumo_energetico."""
    coleccion = db.collection('consumo_energetico')
    
    # Recuperar todos los documentos de la colección
    documentos = coleccion.stream()  # O usar .get()

    print("Datos obtenidos de la base de datos:")
    for doc in documentos:
        data = doc.to_dict()  # Convertir el documento en diccionario
        if data and "consumo_w" in data:
            print(f"ID: {doc.id}, Vatios: {data['consumo_w']}")
        else:
            print(f"ID: {doc.id}, Datos incompletos o vacíos.")



def obtener_datos_voltaje():
    coleccion = db.collection('consumo_energetico').stream()
    
    # Recuperar todos los documentos
    documentos = coleccion.stream()
    
    vatios = []
    for doc in documentos:
        datos = doc.to_dict()
        if "consumo_w" in datos:
            vatios.append(datos["consumo_w"])
    
    return vatios


def exit_program():
    print("Saliendo del programa...")
    global running
    running = False  # Detiene el bucle principal

# Indica si el programa está en ejecución
running = True

'''
# Asignar teclas para funciones
keyboard.add_hotkey("space", toggle_state)  # Presiona 'espacio' para alternar el estado
keyboard.add_hotkey("q", exit_program)    # Presiona 'q' para salir del programa
keyboard.add_hotkey("g", lambda: guardar_datos_firebase(on, w, mA, V)) # Usar lambda para pasar parámetros
keyboard.add_hotkey("d", obtener_todos_los_datos)  # Presiona 'espacio' para alternar el estado


# Bucle principal
while running:
    pass
'''