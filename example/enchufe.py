from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, PLUGIP, PLUGKEY, PLUGVERS, USERNAME, PASSWORD, DEVICE_ID
import logging
import keyboard
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
)
import tuyapower
from firebase_config import inicializar_firebase
import time

# Inicializar Firebase
db = inicializar_firebase()

# Conectar a la API de Tuya
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, AuthType.CUSTOM)
openapi.connect(USERNAME, PASSWORD)

logging.basicConfig(level=logging.DEBUG)

# Variable de control
flag = False

# Obtener datos del enchufe inteligente
on, w, mA, V, err = tuyapower.deviceInfo(DEVICE_ID, PLUGIP, PLUGKEY, PLUGVERS)

def guardar_datos_firebase(on, w, mA, V):
    """Guardar datos en Firestore."""
    coleccion = db.collection('consumo_energetico')
    datos = {
        "estado": on,
        "consumo_w": w,
        "corriente_mA": mA,
        "voltaje_V": V,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
    }
    coleccion.add(datos)
    print(f"Datos guardados en Firebase: {datos}")


def obtener_todos_los_datos():
    """Obtiene todos los documentos de la colección consumo_energetico."""
    coleccion = db.collection('consumo_energetico')
    
    # Recuperar todos los documentos de la colección
    documentos = coleccion.stream()
    
    print("Datos obtenidos de la base de datos:")
    for doc in documentos:
        print(f"ID: {doc.id}, Datos: {doc.to_dict()}")


def toggle_state():
    """
    Alterna el estado del flag y envía comandos al dispositivo para encender/apagar.
    """
    global flag
    flag = not flag  # Alterna el estado del flag

    # Enviar comando para cambiar el estado
    commands = {'commands': [{'code': 'switch_1', 'value': flag}]}
    openapi.post(f'/v1.0/iot-03/devices/{DEVICE_ID}/commands', commands)

    print(f"El estado del enchufe se ha cambiado a: {'Encendido' if flag else 'Apagado'}")


def exit_program():
    """Salir del programa."""
    print("Saliendo del programa...")
    global running
    running = False  # Detiene el bucle principal

# Indica si el programa está en ejecución
running = True

# Asignar teclas para funciones
keyboard.add_hotkey("space", toggle_state)  # Presiona 'espacio' para alternar el estado
keyboard.add_hotkey("q", exit_program)    # Presiona 'q' para salir del programa
keyboard.add_hotkey("g", guardar_datos_firebase(on, w, mA, V))

# Mensaje inicial
print("Presiona 'espacio' para alternar el estado del enchufe o 'q' para salir del programa.")

# Bucle principal
while running:
    pass
