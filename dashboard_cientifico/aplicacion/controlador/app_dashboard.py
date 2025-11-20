from pathlib import Path
import streamlit as st
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.vista.vista import introduccion_general
from dashboard_cientifico.aplicacion.modelo.carga_datos import (cargar_datos,
                                                                generar_json,
                                                                obtener_archivos_csv)

from dashboard_cientifico.aplicacion.config.settings import RUTA_ARCHIVOS

CARGA_ID_POSIBLES={
                "Mayo 2021": "202105","Junio 2021": "202106",
                "Julio 2021": "202107","Agosto 2021": "202108",
                "Septiembre 2021": "202109","Octubre 2021": "202110",
                "Noviembre 2021": "202111","Diciembre 2021": "202112"
                }

CARGA_ID_POSIBLES=[
                "Mayo 2021 -202105","Junio 2021 -202106",
                "Julio 2021 -202107","Agosto 2021 -202108",
                "Septiembre 2021 -202109","Octubre 2021 -202110",
                "Noviembre 2021 -202111","Diciembre 2021 -202112"
                ]



configura_streamlit()

st.title("Dashboard Científico")

st.sidebar.title("Menú")
st.sidebar.header("Gestión de Datos")
st.sidebar.subheader("Cargar Nuevo CSV")

archivos_disponibles = obtener_archivos_csv()

if not archivos_disponibles:  
    archivo_seleccionado = None
    carga_id_seleccionado = None
    st.sidebar.warning(f"No se encontraron archivos CSV")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox(
    "Seleccione el archivo a cargar:",
    archivos_disponibles
)

archivo_seleccionado= Path(f"{RUTA_ARCHIVOS}/{archivo_seleccionado}")

carga_id_seleccionado = st.sidebar.selectbox(
    "Seleccione el ID de Carga:",
    CARGA_ID_POSIBLES
)

carga_id_seleccionado=carga_id_seleccionado.split('-')[1].strip()

if st.sidebar.button("Cargar datos", type='primary'):
    num_filas=cargar_datos(archivo_seleccionado,carga_id_seleccionado)
    st.success(num_filas)

    datos_eliminados, datos_exportados = generar_json()
    st.success(datos_exportados)

    if datos_eliminados:
        st.warning(datos_eliminados)

    
pagina=st.sidebar.selectbox("Selecciona página", [
    "Introducción",
    "Configurar semana", 
    "Agrupar"
    ])

introduccion_general()
