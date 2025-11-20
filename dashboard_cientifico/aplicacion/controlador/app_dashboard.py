from pathlib import Path
import streamlit as st
from dashboard_cientifico.aplicacion.config.settings import (RUTA_ARCHIVO_ENTRADA,
                                                             CARGA_ID_INICIAL)

from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.vista.vista import introduccion_general
from dashboard_cientifico.aplicacion.modelo.carga_datos import (cargar_datos,
                                                                generar_json,
                                                                obtener_archivos_csv,
                                                                verificar_db,
                                                                reset_datos,
                                                                crear_tabla_carga_ids)

from dashboard_cientifico.aplicacion.config.settings import RUTA_ARCHIVOS

CARGA_ID_POSIBLES=[
                "Mayo 2021 -202105","Junio 2021 -202106",
                "Julio 2021 -202107","Agosto 2021 -202108",
                "Septiembre 2021 -202109","Octubre 2021 -202110",
                "Noviembre 2021 -202111","Diciembre 2021 -202112"
                ]



configura_streamlit()
estado: dict = verificar_db()

st.title("Dashboard Científico")


def _menu_normal() -> None:
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
                CARGA_ID_POSIBLES
            )

            carga_id_seleccionado=carga_id_seleccionado.split('-')[1].strip()

            if st.button("Cargar datos", type='primary'):
                num_filas=cargar_datos(archivo_seleccionado,carga_id_seleccionado)
                st.success(num_filas)

                datos_eliminados, datos_exportados = generar_json()
                st.success(datos_exportados)

                if datos_eliminados:
                    st.warning(datos_eliminados)

        with st.expander("Eliminar datos"):
            st.info("Aquí se eliminan los datos del mes seleccionado")                    

        with st.expander("Datos originales"):
            pass

        with st.expander("Reset datos"):
            pass


def _menu_iniciar_datos() -> str:
    mensajes_carga_inicial = []
    with st.expander("Carga inicial"):
        if st.button("Cargar datos", type='primary'):
            mensaje_reset = reset_datos()
            mensajes_carga_inicial.append(f"RESET: {mensaje_reset}")
            
            mensaje_cargar = cargar_datos(RUTA_ARCHIVO_ENTRADA, CARGA_ID_INICIAL)
            mensajes_carga_inicial.append(f"CARGA: {mensaje_cargar}")

            mensaje_ids = crear_tabla_carga_ids()
            mensajes_carga_inicial.append(f"CARGA_IDS: {mensaje_ids}")

            datos_eliminados_json, datos_exportados_json=generar_json()
            mensajes_carga_inicial.append(f"JSON Exportado: {datos_exportados_json}")

            if datos_eliminados_json:
                mensajes_carga_inicial.append(f"JSON Eliminado: {datos_eliminados_json}")

    return "\n\n".join(mensajes_carga_inicial)

mensajes_total_carga=""

match estado['final']:
    case True:
        introduccion_general()
    case False:
        # introduccion_general()
        pass

with st.sidebar:
    st.title("Menú")
    
    match estado['final']:
        case True:
            _menu_normal()
        case False:
            mensajes_total_carga=_menu_iniciar_datos()

if mensajes_total_carga:
    st.info(mensajes_total_carga)
    if st.button("Continuar...", type='primary'):
        st.rerun()


