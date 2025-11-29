import pandas as pd
import streamlit as st
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME

from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.vista.vista import (introduccion_general,
                                                         introduccion_inicial)

from dashboard_cientifico.aplicacion.modelo.carga_datos import (verificar_db,
                                                                obtener_datos_completos,
                                                                inicializar_dataframe)



# Funciones

def _inicializacion_variables_state():
    if CLAVE_DATAFRAME not in st.session_state:
            st.session_state[CLAVE_DATAFRAME] = None

    if 'menu_refresh_key' not in st.session_state:
        st.session_state['menu_refresh_key'] = 0

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

inicializar_dataframe()



# Tareas iniciales

configura_streamlit()
_inicializacion_variables_state()

estado: dict = verificar_db()

if estado['final']:
    inicializar_dataframe()
    introduccion_general()
else:
    introduccion_inicial()
