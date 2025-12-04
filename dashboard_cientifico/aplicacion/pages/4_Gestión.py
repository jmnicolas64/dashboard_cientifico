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

from dashboard_cientifico.aplicacion.vista.vista import (mostrar_mensajes_y_continuar,
                                                         mostrar_mensaje_con_continuacion,
                                                         lista_meses_cargados)

from dashboard_cientifico.aplicacion.modelo.carga_datos import (cargar_datos,
                                                                generar_json,
                                                                obtener_archivos_csv,
                                                                verificar_db,
                                                                reset_datos,
                                                                crear_tabla_carga_ids,
                                                                obtener_cargas_pendientes,
                                                                dame_carga_id_mes,
                                                                eliminar_carga,
                                                                inicializar_dataframe)


def _menu_normal() -> None:
    st.info("Carga y actualización de los datos de la BD")

    mostrar_mensaje_con_continuacion('mensaje_eliminacion', 'eliminacion_terminada')
    mostrar_mensajes_y_continuar('menu_num_filas', 'menu_datos_eliminados', 'menu_datos_exportados','gestion_terminada')

    with st.expander("Cargar Nuevo CSV", expanded=st.session_state['cargar_nuevo_csv']):
        archivos_disponibles = obtener_archivos_csv()

        if CLAVE_DATAFRAME not in st.session_state or st.session_state[CLAVE_DATAFRAME].empty:
            s_principal_cargas = pd.Series([], dtype='object')
        else:
            df_principal = st.session_state[CLAVE_DATAFRAME]
            s_principal_cargas = pd.Series(df_principal['carga_id'].unique())

        carga_id_posibles=obtener_cargas_pendientes(s_principal_cargas)

        if not archivos_disponibles:  
            archivo_seleccionado = None
            carga_id_seleccionado = None
            st.warning(f"No se encontraron archivos CSV")
        
        archivo_seleccionado = st.selectbox(
            "Seleccione el archivo a cargar:",
            archivos_disponibles,
            key=f"archivo_select_{st.session_state['menu_refresh_key']}"
        )

        archivo_seleccionado= Path(f"{RUTA_ARCHIVOS}/{archivo_seleccionado}")

        carga_id_seleccionado = st.selectbox(
            "Seleccione el ID de Carga:",
            carga_id_posibles,
            key=f"carga_id_select_{st.session_state['menu_refresh_key']}"
        )


        carga_id_mes=dame_carga_id_mes(carga_id_seleccionado)
        carga_id_seleccionado=str(carga_id_seleccionado)

        if st.button("Cargar datos", type='primary', key="btn_carga_normal"):
            st.session_state['menu_num_filas'] = cargar_datos(archivo_seleccionado,carga_id_mes, carga_id_seleccionado)
            st.session_state['menu_datos_eliminados'], st.session_state['menu_datos_exportados'] = generar_json()
            del st.session_state[CLAVE_DATAFRAME]
            st.session_state['menu_refresh_key'] += 1
            st.rerun()              

    with st.expander("Eliminar datos", expanded=st.session_state['eliminar_datos']):
        st.info("Aquí se eliminan los datos del mes seleccionado")

        meses_existentes = []
        df_mes_carga = None

        if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
            df_principal = st.session_state[CLAVE_DATAFRAME]
            df_mes_carga = df_principal[['mes', 'carga_id']].drop_duplicates()
            df_mes_carga.sort_values(by='carga_id', ascending=False, inplace=True)

            meses_existentes = list(df_mes_carga['mes'].unique())
            
            mes_seleccionado = st.selectbox(
                "Seleccione el ID de Carga:",
                meses_existentes,
                key=f"mes_select_{st.session_state['menu_refresh_key']}", 
                on_change=lambda: setattr(st.session_state, 'eliminar_datos', True) 
            )

            carga_id_a_eliminar: str = df_mes_carga[df_mes_carga['mes'] == mes_seleccionado]['carga_id'].iloc[0]
            mes_seleccionado = str(mes_seleccionado)

            if st.button("Eliminar mes", type='primary', key="btn_eliminar_mes"):
                mensage_elim: str = eliminar_carga(carga_id_a_eliminar, mes_seleccionado)
                st.session_state['mensaje_eliminacion'] = mensage_elim
                
                del st.session_state[CLAVE_DATAFRAME]
                st.session_state['menu_refresh_key'] += 1
                st.session_state['eliminar_datos'] = False
                st.rerun()
    
    with st.expander("Reset datos", expanded=st.session_state['reset_datos']):
        st.info("Esta opción vuelve la aplicación a la 'Carga inicial'")

        if st.button("Reset...", type='primary', ):
            db: Path=RUTA_DB / NOMBRE_DB
            try:
                    if os.path.exists(db):
                        os.unlink(db)

                    if CLAVE_DATAFRAME in st.session_state:
                        del st.session_state[CLAVE_DATAFRAME]
                        
                    st.session_state['menu_refresh_key'] += 1
                    st.session_state['reset_datos'] = False

                    st.rerun()

            except PermissionError:
                st.error(f"Error de Permiso: No se pudo eliminar '{NOMBRE_DB}'. Asegúrate de que no esté siendo utilizada por otra aplicación o conexión.")
                
            except FileNotFoundError:
                st.warning(f"El archivo '{NOMBRE_DB}' no se encontró durante el intento de eliminación.")

            except Exception as e:
                st.error(f"Ocurrió un error inesperado al resetear el sistema: {e}")


def _menu_iniciar_datos():
    mensajes_carga_inicial = []

    with st.expander("Carga inicial"):
        if st.button("Cargar datos", type='primary', key="btn_carga_inicial"):
            mensaje_reset = reset_datos()
            mensajes_carga_inicial.append(f"1.RESET: {mensaje_reset}")

            mensaje_ids = crear_tabla_carga_ids()
            mensajes_carga_inicial.append(f"2.CARGA_IDS: {mensaje_ids}")
            
            mensaje_cargar = cargar_datos(RUTA_ARCHIVO_ENTRADA, CARGA_ID_INICIAL,"")
            mensajes_carga_inicial.append(f"3. {mensaje_cargar}")

            datos_eliminados_json, datos_exportados_json=generar_json()
            mensajes_carga_inicial.append(f"4.JSON Exportado: {datos_exportados_json}")

            if datos_eliminados_json:
                mensajes_carga_inicial.append(f"5.JSON Eliminado: {datos_eliminados_json}")

            st.session_state['mensajes_carga_inicial'] = "\n\n".join(mensajes_carga_inicial)
            st.session_state['menu_refresh_key'] += 1
            st.rerun()

    return


configura_streamlit()

estado: dict = verificar_db()

st.title("Dashboard Covid")
st.header("Gestión de datos")

if estado['final']:
    inicializar_dataframe()
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
    _menu_normal()       
else:
    _menu_iniciar_datos()

mostrar_mensaje_con_continuacion('mensajes_carga_inicial', 'carga_finalizada_y_lista')


