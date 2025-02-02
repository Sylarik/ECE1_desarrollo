import streamlit as st
from enchufe import toggle_state, obtener_datos_por_intervalo, estado
from gasto import calcular_gasto_total
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

from env import ESIOS_API_KEY

st.title("Monitorizacion consumo energetico")

st.subheader("Control estado del enchufe: encendido/apagado")
# Botón para encender el enchufe
if st.button("Enchufe"):
    toggle_state()
    if estado():
        st.write("encendido")
    else:
        st.write("apagado")


# Título de la aplicación
st.subheader("Consumo energetico temporal")
st.write("Selecciona el rango de fechas en el que quieres ver el consumo de tu dispositivo")
# Selección de intervalo de tiempo
fecha_inicio = st.date_input("Fecha de inicio")
print(fecha_inicio)
fecha_fin = st.date_input("Fecha de fin")

fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')


# Botón para obtener datos
if st.button("Generar gráfica"):
    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser mayor que la fecha de fin")
    else:
        # Obtener datos de Firebase
        datos = obtener_datos_por_intervalo(fecha_inicio, fecha_fin)
        print(datos)

        if datos:
            # Convertir los datos a un DataFrame
            df = pd.DataFrame(datos)

            # Verificar que el campo 'timestamp' existe y convertirlo a datetime
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            else:
                st.error("El campo 'timestamp' no está presente en los datos.")
                st.stop()

            # Ordenar los datos por timestamp
            df = df.sort_values('timestamp')

            # Introducir huecos si la diferencia entre timestamps es mayor a 10 minutos
            max_interval = timedelta(minutes=60)
            df['diff'] = df['timestamp'].diff()  # Calcula la diferencia entre timestamps
            df.loc[df['diff'] > max_interval, ['consumo_w']] = None  # Introduce NaN en huecos grandes

            # Eliminar la columna 'diff' para limpiar el DataFrame
            df.drop(columns=['diff'], inplace=True)



            # Crear la gráfica con st.line_chart
            st.line_chart(
                data=df.set_index('timestamp')['consumo_w'],  # Usar 'timestamp' como índice
                use_container_width=True
            )

            gasto_total = calcular_gasto_total(ESIOS_API_KEY, fecha_inicio, fecha_fin)
            st.write("Gasto en este intervalo:", gasto_total)
        else:
            st.error("No se encontraron datos en el intervalo seleccionado.")