import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
from dashboard_cientifico.aplicacion.modelo.funciones_graficos import obtener_datos_agrupados
from dashboard_cientifico.aplicacion.vista.vista import lista_meses_cargados


# =========================================================================
# FUNCIONES DE VISTA (Presentación)
# =========================================================================

def dibujar_tabla_agrupada(df_agrupado: pd.DataFrame):
    """Maneja el dibujo del resultado de la agrupación en Streamlit."""
    st.dataframe(df_agrupado, width='stretch')
    st.info(f"Tabla generada con **{len(df_agrupado)}** filas.")


def dibujar_box_plot(df: pd.DataFrame, columna_agrupacion: str):
    """Muestra un gráfico de cajas para visualizar la distribución de IA14 por grupo."""
    st.subheader("Distribución de IA14 por Grupo (Box Plot)")
    
    # Suponemos que queremos ver la distribución de 'ia14'
    fig = px.box(
        df,
        x=columna_agrupacion,
        y='ia14',
        title=f"Distribución de la Incidencia Acumulada (IA14) por {columna_agrupacion}",
        points="all",  # Muestra los puntos individuales
        labels={'ia14': 'IA14 (Casos/100k hab.)', columna_agrupacion: columna_agrupacion},
        color=columna_agrupacion
    )
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig, width='stretch')


# =========================================================================
# FLUJO PRINCIPAL (Controlador)
# =========================================================================

configura_streamlit()
st.title("🔬 Análisis Detallado de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Agrupación y Agregación", "Filtrado Rápido"])

    # --- PESTAÑA 1: AGRUPACIÓN Y AGREGACIÓN ---
    with tab1:
        st.subheader("Agrupación y Sumario de Datos")
        
        columnas_disponibles = [col for col in df.columns if col not in ['daily_cases_avg7', 'ia14', 'daily_cases', 'date']]
        
        columna_seleccionada = st.selectbox(
            "Seleccione la columna para agrupar:",
            columnas_disponibles,
            key='select_agrupacion'
        )

        # 🚨 Nuevo: Dibujamos el Box Plot basado en el DataFrame principal y el grupo
        dibujar_box_plot(df, columna_seleccionada) 
        
        # Separación visual
        st.markdown("### Resumen Tabular") 
        
        if st.button("Ejecutar Agrupación y Suma", type='primary', key="btn_ejecutar_agrupacion"):
            # 1. Llamada al Servicio (Modelo)
            df_agrupado = obtener_datos_agrupados(df, columna_seleccionada)
            
            # 2. Llamada a la Vista (Tabla)
            dibujar_tabla_agrupada(df_agrupado)

    # --- PESTAÑA 2: FILTRADO RÁPIDO ---
    # ... (El código de filtrado permanece sin cambios) ...

else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")
