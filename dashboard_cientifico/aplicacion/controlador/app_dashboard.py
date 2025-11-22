from pathlib import Path
import os
from typing import List
import numpy as np
import pandas as pd
import streamlit as st
from dashboard_cientifico.aplicacion.config.settings import (RUTA_DB,
                                                             NOMBRE_DB,
                                                             RUTA_ARCHIVO_ENTRADA,
                                                             CARGA_ID_INICIAL,
                                                             CLAVE_DATAFRAME)

from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.vista.vista import introduccion_general,introduccion_inicial

from dashboard_cientifico.aplicacion.modelo.carga_datos import (cargar_datos,
                                                                generar_json,
                                                                obtener_archivos_csv,
                                                                verificar_db,
                                                                reset_datos,
                                                                crear_tabla_carga_ids,
                                                                obtener_datos_completos,
                                                                obtener_cargas_pendientes,
                                                                dame_carga_id_mes)

from dashboard_cientifico.aplicacion.config.settings import RUTA_ARCHIVOS

configura_streamlit()
estado: dict = verificar_db()

st.title("Dashboard Científico")


def _inicializar_dataframe():
    if CLAVE_DATAFRAME not in st.session_state:
        df = obtener_datos_completos() 
        
        st.session_state[CLAVE_DATAFRAME] = df
        
        if df.empty:
            st.session_state['datos_cargados'] = False
            # mostrar un mensaje de error aquí
        else:
            st.session_state['datos_cargados'] = True


def _cargas_pendientes() -> List[str]:
    if CLAVE_DATAFRAME not in st.session_state or st.session_state[CLAVE_DATAFRAME].empty:
        s_principal_cargas = pd.Series([], dtype='object')
    else:
        df_principal = st.session_state[CLAVE_DATAFRAME]
        s_principal_cargas = pd.Series(df_principal['carga_id'].unique())

    cargas_pendientes=obtener_cargas_pendientes(s_principal_cargas)

    return cargas_pendientes


def _menu_normal() -> tuple[str, str, str]:
    num_filas: str = ""
    datos_eliminados: str = ""
    datos_exportados: str = ""
    
    with st.expander("Dashboard"):
        pagina=st.selectbox("Selecciona página", [
            "Introducción",
            "Configurar semana", 
            "Agrupar"
            ])

    with st.expander("Gestión de Datos"):
        st.info("Carga y actualización de los datos de la BD")
        with st.expander("Cargar Nuevo CSV"):
            archivos_disponibles = obtener_archivos_csv()
            carga_id_posibles=_cargas_pendientes()

            if not archivos_disponibles:  
                archivo_seleccionado = None
                carga_id_seleccionado = None
                st.warning(f"No se encontraron archivos CSV")
                st.stop()

            archivo_seleccionado = st.selectbox(
                "Seleccione el archivo a cargar:",
                archivos_disponibles
            )

            archivo_seleccionado= Path(f"{RUTA_ARCHIVOS}/{archivo_seleccionado}")

            carga_id_seleccionado = st.selectbox(
                "Seleccione el ID de Carga:",
                carga_id_posibles
            )

            carga_id_mes=dame_carga_id_mes(carga_id_seleccionado)

            if st.button("Cargar datos", type='primary'):
                num_filas: str = cargar_datos(archivo_seleccionado,carga_id_mes)

                datos_eliminados, datos_exportados = generar_json()   

        with st.expander("Eliminar datos"):
            st.info("Aquí se eliminan los datos del mes seleccionado")                    

        
        with st.expander("Reset datos"):
            st.info("Esta opción vuelve la aplicación a la 'Carga inicial'")

            if st.button("Reset...", type='primary'):
                db: Path=RUTA_DB / NOMBRE_DB
                os.unlink(db)
                st.rerun()

    return num_filas, datos_eliminados, datos_exportados

def _menu_iniciar_datos() -> str:
    mensajes_carga_inicial = []

    with st.expander("Carga inicial"):
        if st.button("Cargar datos", type='primary'):
            mensaje_reset = reset_datos()
            mensajes_carga_inicial.append(f"1.RESET: {mensaje_reset}")
            
            mensaje_cargar = cargar_datos(RUTA_ARCHIVO_ENTRADA, CARGA_ID_INICIAL)
            mensajes_carga_inicial.append(f"2.CARGA: {mensaje_cargar}")

            mensaje_ids = crear_tabla_carga_ids()
            mensajes_carga_inicial.append(f"3.CARGA_IDS: {mensaje_ids}")

            datos_eliminados_json, datos_exportados_json=generar_json()
            mensajes_carga_inicial.append(f"4.JSON Exportado: {datos_exportados_json}")

            if datos_eliminados_json:
                mensajes_carga_inicial.append(f"5.JSON Eliminado: {datos_eliminados_json}")

            _inicializar_dataframe()

    return "\n\n".join(mensajes_carga_inicial)


mensajes_total_carga, num_filas, datos_eliminados, datos_exportados = [None]*4

if estado['final']:
    _inicializar_dataframe()
    introduccion_general()

    with st.sidebar:
        st.title("Menú")
        num_filas, datos_eliminados, datos_exportados = _menu_normal()
        
else:
    introduccion_inicial()

    with st.sidebar:
        st.title("Menú")
        mensajes_total_carga = _menu_iniciar_datos()

if mensajes_total_carga:
    st.info(mensajes_total_carga)
    if st.button("Continuar...", type='primary'):
        st.rerun()

if num_filas:
    st.success(num_filas)

if datos_exportados:
    st.success(datos_exportados)

if datos_eliminados:
    st.warning(datos_eliminados)

