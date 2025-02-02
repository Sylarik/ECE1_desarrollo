from datetime import datetime, timedelta
import requests
from enchufe import obtener_datos_por_intervalo


def obtener_precios_por_intervalo(token, fecha_inicio, fecha_fin):

    url = f"https://api.esios.ree.es/indicators/600?start_date={fecha_inicio.isoformat()}&end_date={fecha_fin.isoformat()}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": token
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        datos = response.json()
        precios = datos["indicator"]["values"]
        
        precios_dict = {}
        for precio in precios:
            timestamp = datetime.strptime(precio["datetime"][:19], "%Y-%m-%dT%H:%M:%S")  # Convertir timestamp a datetime
            precios_dict[timestamp] = precio["value"] / 1000000  # Convertir de €/MWh a €/Wh
        
        return precios_dict
    
    else:
        print(f"Error al obtener precios de ESIOS: {response.status_code}")
        return None


def obtener_consumos_por_intervalo(fecha_inicio, fecha_fin):
    datos = obtener_datos_por_intervalo(fecha_inicio, fecha_fin)
    consumos = [{"timestamp": datetime.strptime(dato["timestamp"], "%Y-%m-%d %H:%M:%S"), "consumo_w": dato["consumo_w"]}
                for dato in datos if "consumo_w" in dato and "timestamp" in dato]
    return consumos


def calcular_gasto_total(token, fecha_inicio, fecha_fin):
    # Obtener los valores de consumo en vatios y sus timestamps
    consumos = obtener_consumos_por_intervalo(fecha_inicio, fecha_fin)
    if not consumos:
        print("No se encontraron datos de consumo en la base de datos.")
        return

    # Obtener los precios históricos en el mismo intervalo
    precios = obtener_precios_por_intervalo(token, fecha_inicio, fecha_fin)
    if not precios:
        print("No se pudieron obtener los precios de electricidad en el intervalo seleccionado.")
        return

    # Ajustar el consumo en vatios a Wh para intervalos de 5 minutos y calcular el costo con el precio en cada momento
    intervalo_minutos = 5
    gasto_total = 0

    for consumo in consumos:
        timestamp = consumo["timestamp"]
        consumo_w = consumo["consumo_w"]
        
        # Buscar el precio más cercano al timestamp del consumo
        precio_actual = min(precios.keys(), key=lambda t: abs((t - timestamp).total_seconds()))
        precio_en_momento = precios[precio_actual]
        
        # Convertir a Wh y calcular el costo
        energia_wh = consumo_w * (intervalo_minutos / 60)
        costo = energia_wh * precio_en_momento

        print("fecha:", precio_actual)
        print("precio en esa hora:", precio_en_momento)
        print("consumo_w:", consumo_w)
        print("energia_wh:", energia_wh)
        print("costo:", costo, "\n")

        gasto_total += costo

    print(f"Gasto total estimado: {gasto_total:.6f} €")
    return gasto_total

