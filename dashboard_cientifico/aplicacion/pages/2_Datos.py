# C:\...\aplicacion\pages\3_Datos.py (MODIFICADO)

import streamlit as st
import pandas as pd
from dashboard_cientifico.aplicacion.config.settings import (CLAVE_DATAFRAME,
                                                             RUTA_DESCARGAS,
                                                             CARPETA_DESCARGAS,
                                                             NOMBRE_JSON_PEDIDO,
                                                             NOMBRE_CSV_DESCARGAS)

from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_datos_filtrados,
                                                                       preparar_datos_csv,
                                                                       cargar_json,
                                                                       guardar_datos_csv)

from dashboard_cientifico.aplicacion.vista.vista import lista_meses_cargados


configura_streamlit()
st.header("Visualización de Datos")

if (CLAVE_DATAFRAME in st.session_state and 
    st.session_state[CLAVE_DATAFRAME] is not None 
    and not st.session_state[CLAVE_DATAFRAME].empty):

    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)

    st.subheader("JSON generado (ejercicio 1)")
    with st.expander("Ver JSON", expanded=False):
        datos, error = cargar_json(RUTA_DESCARGAS / NOMBRE_JSON_PEDIDO)

        if error:
            st.error(f"Error al cargar los datos: {error}")
        elif datos:
            st.subheader("Contenido del JSON")
            st.json(datos)

    #st.markdown("---")

    st.subheader("Filtrar datos originales")

    col1, col2 = st.columns([1, 2])

    columnas_prioritarias = ['mes', 'ccaa', 'province', 'date']
    columnas_actuales = set(df.columns.tolist())

    resto_columnas = [col
                      for col in df.columns.tolist()
                      if col not in set(columnas_prioritarias)
                      ]

    columnas_ordenadas = [col 
                          for col in columnas_prioritarias 
                          if col in columnas_actuales
                          ] + resto_columnas

    with col1:
        columna_a_filtrar = st.selectbox("Columna", columnas_ordenadas)

    with col2:
        valores_unicos = [''] + df[columna_a_filtrar].unique().tolist()
        valor_seleccionado = st.selectbox(f"Filtrar por {columna_a_filtrar}", valores_unicos)

    df_filtrado = obtener_datos_filtrados(df, columna_a_filtrar, valor_seleccionado, columnas_ordenadas)
    
    st.dataframe(df_filtrado, width='stretch')
    
    datos_exportables = preparar_datos_csv(df_filtrado)

    if st.button("Exportar Datos en CSV"):
        ruta = guardar_datos_csv(df_filtrado)
        st.success(f"Datos exportados con éxito en la ruta: {CARPETA_DESCARGAS}/{NOMBRE_CSV_DESCARGAS}")
    
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Gestión'.")
