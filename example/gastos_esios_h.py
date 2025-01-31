import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io  # Para manejar archivos en memoria
from env import ESIOS_API_KEY
#from openai import OpenAI

# API key y headers para ESIOS y OpenAI

# Función para obtener datos de la API de ESIOS con un rango de fechas
def obtener_datos_esios(fecha_inicio, fecha_fin):
    headers = {
        'Accept': 'application/json; application/vnd.esios-api-v1+json',
        'Content-Type': 'application/json',
        'x-api-key': ESIOS_API_KEY
    }

    url = f'https://api.esios.ree.es/indicators/600?start_date={fecha_inicio}&end_date={fecha_fin}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"Error al conectarse a la API de ESIOS. Código de estado: {response.status_code}")
        return pd.DataFrame()  # Retorna un DataFrame vacío si falla la solicitud

    data = response.json()

    precios_horarios = []
    if 'indicator' in data and 'values' in data['indicator']:
        for item in data['indicator']['values']:
            if item['geo_name'] == "España":
                fecha = item['datetime']
                precio = item['value']
                precios_horarios.append({'Fecha': fecha, 'Precio (€/MWh)': precio})
    else:
        st.error("No se encontraron datos de precios en la respuesta de la API.")
        return pd.DataFrame()

    df = pd.DataFrame(precios_horarios)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Fecha'] = df['Fecha'].dt.tz_localize(None)
    return df

# Función para mostrar un gráfico de los datos
def mostrar_grafico(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Fecha'], df['Precio (€/MWh)'], label='Precio (€/MWh)', color='blue')
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Precio (€/MWh)')
    plt.title('Precios de la electricidad en España')
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)


# Interfaz de Streamlit
st.title("Precios de la Electricidad y Recomendación para Gimnasio")

# Seleccionar rango de fechas
fecha_inicio = st.date_input("Fecha de inicio", datetime.today() - timedelta(days=1))
fecha_fin = st.date_input("Fecha de fin", datetime.today())

if st.button("Obtener datos y generar recomendación"):
    fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S')
    fecha_fin_str = fecha_fin.strftime('%Y-%m-%dT%H:%M:%S')

    df = obtener_datos_esios(fecha_inicio_str, fecha_fin_str)

    if not df.empty:
        st.subheader(f"Gráfico del precio de la electricidad por hora en España desde {fecha_inicio_str} hasta {fecha_fin_str}")
        mostrar_grafico(df)


        st.subheader("Recomendación de horario para usar las bicicletas")
       # recomendacion = obtener_recomendacion_gimnasio(df)
        #st.write(recomendacion)
    else:
        st.error("No se encontraron datos para mostrar.")