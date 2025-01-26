from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, PLUGIP, PLUGKEY, PLUGVERS, USERNAME, PASSWORD, DEVICE_ID
from tuya_iot import TuyaOpenAPI, AuthType
import tuyapower
from firebase_config import inicializar_firebase
import time

# Inicializar Firebase
db = inicializar_firebase()

# Conectar a la API de Tuya
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, AuthType.CUSTOM)
openapi.connect(USERNAME, PASSWORD)

def guardar_datos_firebase():
    """Recupera los datos del enchufe inteligente y los guarda en Firestore."""
    # Obtener datos del enchufe inteligente
    on, w, mA, V, err = tuyapower.deviceInfo(DEVICE_ID, PLUGIP, PLUGKEY, PLUGVERS)

    # Imprimir datos en consola
    print(f"Estado: {on}, Consumo (W): {w}, Corriente (mA): {mA}, Voltaje (V): {V} [Error: {err}]")

    # Guardar datos en Firebase
    coleccion = db.collection('consumo_energetico')    #Si no existe la tabla la crea
    datos = {
        "estado": on,
        "consumo_w": w,
        "corriente_mA": mA,
        "voltaje_V": V,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora actual
    }
    coleccion.add(datos)
    print(f"Datos guardados en Firebase: {datos}")

# Ejecutar la función
if __name__ == "__main__":
    guardar_datos_firebase()
