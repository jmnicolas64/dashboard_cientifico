# C:\...\aplicacion\pages\1_Dashboard.py (MODIFICADO)

import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.vista.vista import (lista_meses_cargados,
                                                         dibujar_grafica_acumulados_dia,
                                                         dibujar_grafica_queso_provincia)

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_evolucion_nacional,
                                                                       obtener_ia14_por_ccaa,
                                                                       obtener_acumulados_por_dia_semana,
                                                                       obtener_totales_por_provincia,
                                                                       obtener_max_min_provincia)


# Definición de Métricas para el Menú
METRICAS_EJERCICIOS = {
    "Defunciones": 'num_def', 
    "Casos (Nuevos)": 'new_cases', 
    "Hospitalizados": 'num_hosp', 
    "UCI": 'num_uci'
}

# =========================================================================
# FUNCIONES DE VISTA (Dibujo)
# =========================================================================

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


def ejecutar_ejercicios_2_y_3(df: pd.DataFrame):
    st.subheader("Menú de Visualización (Ejercicios 2 y 3)")
    st.markdown("Utilice el menú para simular la selección de gráficos y mostrar el análisis de Máximos y Mínimos.")
    
    opciones_menu = ["Seleccione una métrica"] + list(METRICAS_EJERCICIOS.keys())
    
    opcion_seleccionada = st.selectbox(
        "¿Qué gráfica quieres visualizar?",
        options=opciones_menu,
        key="menu_ejercicios_dashboard"
    )

    if opcion_seleccionada in METRICAS_EJERCICIOS:
        metrica = METRICAS_EJERCICIOS[opcion_seleccionada]
        
        # --- EJERCICIO 2: GRÁFICAS DE BARRAS (Acumulados por Día) ---
        st.markdown("### Gráfico 1: Acumulado por Día de la Semana (Ejercicio 2)")
        
        # 1. Llamada al Servicio (Modelo)
        df_dia = obtener_acumulados_por_dia_semana(df, metrica)
        
        # 2. Llamada a la Vista
        dibujar_grafica_acumulados_dia(df_dia, metrica)
        
        st.markdown("---")
        
        # --- EJERCICIO 3: GRÁFICAS DE QUESO (Distribución Provincial + Máx/Mín) ---
        st.markdown("### Gráfico 2: Distribución por Provincia y Análisis Máx/Mín (Ejercicio 3)")
        
        # 1. Obtener Totales Provinciales (Servicio)
        df_provincia_total = obtener_totales_por_provincia(df, metrica)
        
        # 2. Obtener Máximo y Mínimo (Servicio)
        max_min_data = obtener_max_min_provincia(df_provincia_total, metrica)
        
        # 3. Dibujar Gráfico de Queso y mostrar texto (Vista)
        dibujar_grafica_queso_provincia(df_provincia_total, metrica, max_min_data)

# =========================================================================
# FLUJO PRINCIPAL (Controlador)
# =========================================================================

configura_streamlit()
st.title("📈 Dashboard")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
    # ... (Reset index y markdown) ...

    # Crear pestañas
    tab1, tab2, tab3 = st.tabs(["Ejercicios del Proyecto", "Evolución Temporal Nacional", "Análisis Geográfico (IA14)"])

    with tab1:
        ejecutar_ejercicios_2_y_3(df) # 🚨 Llamada al nuevo controlador

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