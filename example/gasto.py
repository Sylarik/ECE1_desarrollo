import time
import requests
from firebase_config import inicializar_firebase

ESIOS_API_KEY = '78afc97a1d7ebee5e4acaf9b67c7c1e83164c9f515853c0f78f066bbbfd31712'

def obtener_precio_actual_esios(token):
    """
    Obtiene el precio actual del mercado eléctrico en €/kWh desde la API de ESIOS.
    """
    url = "https://api.esios.ree.es/indicators/600"  # Indicador 600: Precio del mercado mayorista
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        'x-api-key': token
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        precios = datos['indicator']['values']
        if precios:
            precio_actual = precios[-1]['value']  # Último precio disponible
            print(precio_actual)
            return precio_actual / 1000000  # Convertir de €/MWh a €/Wh
    else:
        print(f"Error al conectar con la API de ESIOS: {response.status_code}")
        return None


def obtener_datos_voltaje():
    """
    Recupera los valores de consumo (W) de la base de datos Firestore.
    """
    db = inicializar_firebase()
    coleccion = db.collection('consumo_energetico')
    documentos = coleccion.stream()
    
    consumos = []
    for doc in documentos:
        datos = doc.to_dict()
        if "consumo_w" in datos:
            consumos.append(datos["consumo_w"])
    
    return consumos


def calcular_gasto_total(token):
    """
    Calcula el gasto total en función del consumo en vatios (W) y el precio actual de la electricidad.
    """
    # Obtener los valores de consumo en vatios
    consumos = obtener_datos_voltaje()
    if not consumos:
        print("No se encontraron datos de consumo en la base de datos.")
        return

    # Obtener el precio actual de la electricidad
    precio_actual = obtener_precio_actual_esios(token)
    print(float(precio_actual))
    if precio_actual is None:
        print("No se pudo obtener el precio actual de la electricidad.")
        return

    # Ajustar el consumo en vatios a Wh para intervalos de 5 minutos
    intervalo_minutos = 5
    energia_total_wh = sum(consumo * (intervalo_minutos / 60) for consumo in consumos)

    # Calcular el gasto total
    gasto_total = energia_total_wh * precio_actual  # €/Wh
    print(f"Gasto total estimado: {gasto_total:.2f} €")


# Ejecutar el programa
if __name__ == "__main__":
    calcular_gasto_total(ESIOS_API_KEY)
