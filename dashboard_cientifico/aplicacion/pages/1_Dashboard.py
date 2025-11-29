# C:\...\aplicacion\pages\1_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Asegúrate de que las rutas de importación son correctas
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit
# =========================================================================
# FUNCIONES DE GRÁFICOS
# =========================================================================

configura_streamlit()

def dashboard_evolucion_temporal(df: pd.DataFrame):
    """
    Muestra la evolución temporal de la media móvil de 7 días.
    Demuestra el uso del dato 'daily_cases_avg7' previamente calculado con Pandas.
    """
    st.subheader("Evolución Nacional de Casos Confirmados (Media Móvil 7 Días)")
    st.markdown("_(Visualizando **`daily_cases_avg7`**, calculado con `groupby().transform().rolling().mean()`)_")

    # 1. Preparación de Datos: Agrupar por fecha y sumar las medias móviles a nivel NACIONAL
    # Demuestra el uso de groupby().sum() para agregación final.
    df_nacional = df.groupby('date')[['daily_cases', 'daily_cases_avg7']].sum().reset_index()
    
    # 2. Creación del Gráfico (Plotly Express)
    fig = px.line(
        df_nacional, 
        x='date', 
        y='daily_cases_avg7', 
        title='Casos Diarios Nacionales Suavizados (Media Móvil 7 Días)',
        labels={'date': 'Fecha', 'daily_cases_avg7': 'Casos (Media Móvil)'},
        template='plotly_white',
        line_shape='spline'
    )

    # Añadir la línea de casos diarios crudos como referencia (demuestra el efecto del suavizado)
    fig.add_scatter(
        x=df_nacional['date'], 
        y=df_nacional['daily_cases'], 
        mode='lines', 
        name='Casos Diarios Crudos', 
        line=dict(color='rgba(192, 192, 192, 0.5)', dash='dot') # Gris claro y semi-transparente
    )

    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, width='stretch')


def dashboard_estructura_geografica(df: pd.DataFrame):
    """
    Muestra la distribución geográfica de la IA14 en el último día disponible.
    Demuestra el uso de Pandas 'groupby().agg()' para consolidación final.
    """
    st.subheader("Distribución de la Tasa de Incidencia Acumulada a 14 Días (IA14)")
    st.markdown("_(Visualizando el resultado de la agregación **`groupby().agg('max')`** para la IA14 por CCAA)_")
    
    # 1. Preparación de Datos: Agregación Geográfica
    
    # a) Encontrar el último día disponible
    ultimo_dia = df['date'].max()
    df_ultimo_dia = df[df['date'] == ultimo_dia]
    
    # b) Agrupar por CCAA y obtener el valor MÁXIMO de IA14 para esa CCAA en ese día.
    # El uso de agg() aquí demuestra cómo condensar datos de múltiples provincias en un resumen por CCAA.
    df_ccaa = df_ultimo_dia.groupby('ccaa').agg(
        ia14_max=('ia14', 'max') # Seleccionamos el valor de IA14 más alto de las provincias de esa CCAA
    ).reset_index()

    # Ordenar los datos por IA14 para un gráfico más legible
    df_ccaa = df_ccaa.sort_values(by='ia14_max', ascending=False)
    
    # Mostrar el DataFrame de agregación como prueba del manejo de datos
    with st.expander(f"Ver DataFrame Agregado por CCAA (Último Día: **{ultimo_dia.strftime('%Y-%m-%d')}**):"):
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
    
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, width='stretch')


# =========================================================================
# FLUJO PRINCIPAL DE 1_Dashboard.py
# =========================================================================

st.title("📈 Dashboard")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]

    st.markdown("---")
    
    # Aseguramos que 'date' está presente para las funciones de gráfico
    if 'date' not in df.columns:
        df.reset_index(inplace=True) 

    # Crear pestañas para organizar los gráficos
    tab1, tab2 = st.tabs(["Evolución Temporal Nacional", "Análisis Geográfico (IA14)"])

    with tab1:
        dashboard_evolucion_temporal(df)
    
    with tab2:
        dashboard_estructura_geografica(df)


else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")