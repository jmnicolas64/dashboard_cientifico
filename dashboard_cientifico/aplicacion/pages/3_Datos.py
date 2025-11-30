# C:\...\aplicacion\pages\3_Datos.py (MODIFICADO)

import streamlit as st
import pandas as pd
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.modelo.funciones_graficos import obtener_datos_filtrados, preparar_datos_csv
from dashboard_cientifico.aplicacion.vista.vista import lista_meses_cargados

# =========================================================================
# FLUJO PRINCIPAL (Controlador)
# =========================================================================

# ... (Lógica de configuración y título) ...
configura_streamlit()
st.title("🗄️ Visualización y Exportación de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
    st.subheader("Filtros de Datos")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        columna_a_filtrar = st.selectbox("Columna", df.columns.tolist())
    
    with col2:
        # Obtener valores únicos para el filtro
        valores_unicos = [''] + df[columna_a_filtrar].unique().tolist()
        valor_seleccionado = st.selectbox(f"Filtrar por {columna_a_filtrar}", valores_unicos)

    # 1. Controlador: Llama al Servicio (Modelo) para obtener el DataFrame filtrado
    df_filtrado = obtener_datos_filtrados(df, columna_a_filtrar, valor_seleccionado)
    
    st.markdown("---")
    st.subheader("Datos Resultantes")
    st.dataframe(df_filtrado, width='stretch')
    
    # 2. Controlador: Preparar y mostrar el botón de descarga
    datos_exportables = preparar_datos_csv(df_filtrado)

    st.download_button(
        label="Descargar datos filtrados (CSV)",
        data=datos_exportables,
        file_name='datos_exportados.csv',
        mime='text/csv'
    )
    
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado.")
