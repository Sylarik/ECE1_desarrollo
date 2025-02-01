import streamlit as st
from enchufe import toggle_state, obtener_datos_por_intervalo
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

# Título de la aplicación
st.title("Mi primera aplicación con Streamlit")

# Subtítulo
st.header("¡Bienvenido!")

# Texto introductorio
st.write("Esta es una aplicación simple para mostrar cómo funciona Streamlit.")

# Entrada de texto
nombre = st.text_input("¿Cómo te llamas?", "")

# Botón
if st.button("Saludar"):
    st.success(f"¡Hola, {nombre}! 👋")

# Slider
edad = st.slider("¿Cuál es tu edad?", 0, 100, 25)
st.write(f"Tienes {edad} años.")

######################################################33

# Botón para encender el enchufe
if st.button("Encender Enchufe"):
    toggle_state()
    #st.write(resultado)


# Título de la aplicación
st.title("Gráficas con Intervalos de Tiempo desde Firebase")

# Entradas de usuario
coleccion = st.text_input("Ingresa el nombre de la colección en Firebase", "mi_coleccion")
print("oigenwognognr",coleccion)
# Selección de intervalo de tiempo
fecha_inicio = st.date_input("Fecha de inicio")
print(fecha_inicio)
fecha_fin = st.date_input("Fecha de fin")

'''
# Conversión a formato datetime (Firestore requiere timestamps)
fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
fecha_fin = datetime.combine(fecha_fin, datetime.max.time())
'''

fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

# Columna a graficar
columna = st.text_input("Ingresa el nombre de la columna a graficar", "valor")

# Botón para obtener datos
if st.button("Generar gráfica"):
    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser mayor que la fecha de fin")
    else:
        # Obtener datos de Firebase
        datos = obtener_datos_por_intervalo(coleccion, fecha_inicio, fecha_fin)
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

            # Mostrar los datos procesados para depuración
            st.write("Datos procesados con huecos:")
            st.write(df)

            # Crear la gráfica con st.line_chart
            st.line_chart(
                data=df.set_index('timestamp')['consumo_w'],  # Usar 'timestamp' como índice
                use_container_width=True
            )
        else:
            st.error("No se encontraron datos en el intervalo seleccionado.")
