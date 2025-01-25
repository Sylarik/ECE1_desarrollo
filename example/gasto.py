import time
import requests
from firebase_config import inicializar_firebase

def obtener_precio_actual_esios(token):
    """
    Obtiene el precio actual del mercado eléctrico en €/kWh desde la API de ESIOS.
    """
    url = "https://api.esios.ree.es/indicators/600"  # Indicador 600: Precio del mercado mayorista
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Token token={token}"  # Sustituye {token} por tu token personal
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        # Extraer el precio actual (último dato disponible)
        precios = datos['indicator']['values']
        if precios:
            precio_actual = precios[-1]['value']  # Último precio disponible
            return precio_actual / 1000  # Convertir de €/MWh a €/kWh
    else:
        print(f"Error al conectar con la API de ESIOS: {response.status_code}")
        return None


def obtener_datos_voltaje():
    """
    Recupera los valores de voltaje de la base de datos Firestore.
    """
    db = inicializar_firebase()
    coleccion = db.collection('consumo_energetico')
    
    # Recuperar todos los documentos
    documentos = coleccion.stream()
    
    voltajes = []
    for doc in documentos:
        datos = doc.to_dict()
        if "voltaje_V" in datos:
            voltajes.append(datos["voltaje_V"])
    
    return voltajes


def calcular_gasto_total(token):
    """
    Calcula el gasto total en función del voltaje y el precio actual de la electricidad.
    """
    # Obtener los valores de voltaje
    voltajes = obtener_datos_voltaje()
    if not voltajes:
        print("No se encontraron datos de voltaje en la base de datos.")
        return

    # Obtener el precio actual de la electricidad
    precio_actual = obtener_precio_actual_esios(token)
    if precio_actual is None:
        print("No se pudo obtener el precio actual de la electricidad.")
        return

    # Calcular el gasto total
    gasto_total = sum(voltajes) * precio_actual  # Suponiendo que voltajes está en kWh
    print(f"Gasto total estimado: {gasto_total:.2f} €")


# Ejecutar el programa
if __name__ == "__main__":
    TOKEN_ESIOS = "TU_TOKEN_DE_ESIOS_AQUÍ"  # Sustituye por tu token de ESIOS

    calcular_gasto_total(TOKEN_ESIOS)
