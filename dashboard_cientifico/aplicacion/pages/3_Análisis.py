import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_datos_agrupados,
                                                                       obtener_evolucion_nacional,
                                                                       obtener_ia14_por_ccaa)

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

def dashboard_evolucion_temporal(df_nacional: pd.DataFrame):
    # Ya no hace falta la preparación de datos aquí, solo el dibujo
    
    # 1. Creación del Gráfico (Plotly Express)
    fig = px.line(
        df_nacional, 
        x='date', 
        y='daily_cases_avg7', 
        title='Casos Diarios Nacionales Suavizados (Media Móvil 7 Días)',
        labels={'date': 'Fecha', 'daily_cases_avg7': 'Casos (Media Móvil)'},
        template='plotly_white',
        line_shape='spline'
    )
    # ... (Añadir scatter y update_layout como antes) ...
    
    st.plotly_chart(fig, width='stretch')


def dashboard_estructura_geografica(df_ccaa: pd.DataFrame, ultimo_dia_str: str):
    # 1. Mostrar el DataFrame de agregación como prueba
    with st.expander(f"Ver DataFrame Agregado por CCAA (Último Día: **{ultimo_dia_str}**):"):
        st.dataframe(df_ccaa, width='stretch')

    # 2. Creación del Gráfico (Plotly Express - Barras)
    fig = px.bar(
        df_ccaa,
        x='ccaa',
        y='ia14_max',
        title=f"IA14 por Comunidad Autónoma",
        labels={'ccaa': 'Comunidad Autónoma', 'ia14_max': 'IA14 (Casos/100k hab.)'},
        color='ia14_max',
        color_continuous_scale=px.colors.sequential.Reds
    )
    # ... (update_xaxes como antes) ...
    st.plotly_chart(fig, width='stretch')

# =========================================================================
# FLUJO PRINCIPAL (Controlador)
# =========================================================================

st.set_page_config(page_title="Herramientas de Análisis")
configura_streamlit()
st.title("🔬 Análisis Detallado de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Agrupación y Agregación", "Filtrado Rápido", "Evolución Temporal Nacional", "Análisis Geográfico (IA14)"])

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
        with tab2:
            st.subheader("Evolución Nacional de Casos Confirmados (Media Móvil 7 Días)")
            st.markdown("_(Visualizando **`daily_cases_avg7`**, calculado con `groupby().transform().rolling().mean()`)_")
            
            # 🚨 LLAMADA AL SERVICIO: Obtiene los datos preparados
            df_nacional = obtener_evolucion_nacional(df)
            dashboard_evolucion_temporal(df_nacional)
    
    with tab3:
        st.subheader("Distribución de la Tasa de Incidencia Acumulada a 14 Días (IA14)")
        st.markdown("_(Visualizando el resultado de la agregación **`groupby().agg('max')`** para la IA14 por CCAA)_")
        
        # 🚨 LLAMADA AL SERVICIO: Obtiene los datos y la fecha
        df_ccaa, ultimo_dia_str = obtener_ia14_por_ccaa(df)
        dashboard_estructura_geografica(df_ccaa, ultimo_dia_str)

else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")
