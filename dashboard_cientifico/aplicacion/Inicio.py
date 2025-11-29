from pathlib import Path
import os
from typing import List
import numpy as np
import pandas as pd
import streamlit as st
from dashboard_cientifico.aplicacion.config.settings import (RUTA_DB,
                                                             RUTA_ARCHIVOS,
                                                             NOMBRE_DB,
                                                             RUTA_ARCHIVO_ENTRADA,
                                                             CARGA_ID_INICIAL,
                                                             CLAVE_DATAFRAME)

from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.vista.vista import (introduccion_general,
                                                         introduccion_inicial,
                                                         mostrar_mensajes_y_continuar,
                                                         mostrar_mensaje_con_continuacion)

from dashboard_cientifico.aplicacion.modelo.carga_datos import (cargar_datos,
                                                                generar_json,
                                                                obtener_archivos_csv,
                                                                verificar_db,
                                                                reset_datos,
                                                                crear_tabla_carga_ids,
                                                                obtener_datos_completos,
                                                                obtener_cargas_pendientes,
                                                                dame_carga_id_mes,
                                                                eliminar_carga)



# Funciones

def _inicializacion_variables_state():
    if CLAVE_DATAFRAME not in st.session_state:
            st.session_state[CLAVE_DATAFRAME] = None

    if 'menu_refresh_key' not in st.session_state:
        st.session_state['menu_refresh_key'] = 0

    if 'gestion_datos' not in st.session_state:
        st.session_state['gestion_datos'] = False
    if 'cargar_nuevo_csv' not in st.session_state:
        st.session_state['cargar_nuevo_csv'] = False
    if 'eliminar_datos' not in st.session_state:
        st.session_state['eliminar_datos'] = False
    if 'reset_datos' not in st.session_state:
        st.session_state['reset_datos'] = False               

    if 'mensajes_carga_inicial' not in st.session_state:
        st.session_state['mensajes_carga_inicial'] = ""
    if 'carga_finalizada_y_lista' not in st.session_state:
        st.session_state['carga_finalizada_y_lista'] = ""

    if 'menu_num_filas' not in st.session_state:
        st.session_state['menu_num_filas'] = ""
    if 'menu_datos_eliminados' not in st.session_state:
        st.session_state['menu_datos_eliminados'] = ""
    if 'menu_datos_exportados' not in st.session_state:
        st.session_state['menu_datos_exportados'] = ""

    if 'mensaje_eliminacion' not in st.session_state:
        st.session_state['mensaje_eliminacion'] = ""
    if 'eliminacion_terminada' not in st.session_state:
        st.session_state['eliminacion_terminada'] = ""


def _inicializar_dataframe():
    df = obtener_datos_completos() 
    
    st.session_state[CLAVE_DATAFRAME] = df
    
    if df.empty:
        st.session_state[CLAVE_DATAFRAME] = pd.DataFrame() 
        return

    df['date'] = pd.to_datetime(df['date'], dayfirst=True)

    df['daily_cases_avg7'] = df.groupby('province')['daily_cases'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
    )

    df['daily_deaths_calculated'] = df.groupby('province')['deceased'].diff().fillna(0)

    df['daily_deaths_avg7'] = df.groupby('province')['daily_deaths_calculated'].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    df['cases_per_100k'] = (df['cases_accumulated'] / df['poblacion']) * 100000

    st.session_state[CLAVE_DATAFRAME] = df

# Tareas iniciales

configura_streamlit()
_inicializacion_variables_state()

estado: dict = verificar_db()

if estado['final']:
    _inicializar_dataframe()
    st.title("Bienvenido al Dashboard Científico")
    introduccion_general()
    st.info("Utiliza el menú lateral para gestionar la base de datos o navega a las otras páginas para ver los gráficos.")
    
else:
    # [MANTENER] Si la DB no está lista, dibuja la introducción inicial
    introduccion_inicial()

