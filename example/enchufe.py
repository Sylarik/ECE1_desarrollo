from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, PLUGIP, PLUGKEY, PLUGVERS, USERNAME, PASSWORD, DEVICE_ID
import logging
import time
import keyboard
import sys
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
    TuyaOpenMQ,
    TuyaDeviceManager,
    TuyaHomeManager,
    TuyaDeviceListener,
    TuyaDevice,
    TuyaTokenInfo,
    TUYA_LOGGER,
    device
)
import tuyapower

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY,AuthType.CUSTOM)
openapi.connect(USERNAME, PASSWORD)

import logging

TUYA_LOGGER.setLevel(logging.DEBUG)

#aqui guardamos el estado, lo vatios, miliamperios, voltaje, y si hay algun error.        


print("Presiona la tecla 'espacio' para continuar o 'q' para salir.")
flag = True

def toggle_flag():
    """
    Alterna el estado del flag y ejecuta el comando correspondiente.
    """
    global flag
    flag = not flag  # Alterna el estado del flag
    
    # Comando para enviar el nuevo estado al dispositivo
    commands = {'commands': [{'code': 'switch_1', 'value': flag}]}
    openapi.post(f'/v1.0/iot-03/devices/{DEVICE_ID}/commands', commands)

    # Obtiene la información actual del dispositivo
    on, w, mA, V, err = tuyapower.deviceInfo(DEVICE_ID, PLUGIP, PLUGKEY, PLUGVERS)
    tuyapower.devicePrint(DEVICE_ID, PLUGIP, PLUGKEY, PLUGVERS)

    # Imprime el estado actual
    print(f" state={on}, W={w}, mA={mA}, V={V} [{err}]")

def exit_program():
    """
    Sale del programa limpiamente.
    """
    print("Saliendo del programa...")
    global running
    running = False  # Detiene el bucle principal

# Indica si el programa está en ejecución
running = True

# Asigna las teclas a las funciones
keyboard.add_hotkey("space", toggle_flag)  # Presiona 'espacio' para alternar el estado
keyboard.add_hotkey("q", exit_program)    # Presiona 'q' para salir del programa

# Mensaje inicial para el usuario
print("Presiona 'espacio' para alternar el estado del enchufe o 'q' para salir del programa.")

# Bucle principal
while running:
    pass 
