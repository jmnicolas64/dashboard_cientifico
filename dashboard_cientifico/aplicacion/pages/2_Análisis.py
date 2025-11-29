# C:\...\aplicacion\pages\2_Análisis.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Asegúrate de que las rutas de importación son correctas
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

configura_streamlit()

def analisis_comparativo_boxplot(df: pd.DataFrame):
    """
    Muestra la distribución de la IA14 de las provincias dentro de cada CCAA.
    Demuestra la comparación de distribución estadística.
    """
    st.subheader("Distribución de la Incidencia Acumulada (IA14) por CCAA")
    st.markdown("_(Usando Box Plots para comparar la mediana, cuartiles y valores atípicos de la IA14 entre regiones)_")
    
    # 1. Preparación de Datos (Dominio de Pandas)
    
    # Para el análisis comparativo, filtramos la columna clave (IA14) y la columna de agrupación (ccaa).
    # Como la IA14 es un indicador diario, el boxplot reflejará la dispersión de este indicador
    # a lo largo del tiempo para cada CCAA.
    
    # En este caso, no se necesita pd.melt() ya que los datos ya están en formato largo,
    # con una columna de métrica (ia14) y una columna de categoría (ccaa).
    df_box = df[['ccaa', 'ia14', 'date']].copy()
    
    # Eliminamos valores nulos de IA14 para un Box Plot limpio
    df_box.dropna(subset=['ia14'], inplace=True)
    
    # 2. Creación del Gráfico (Plotly Express - Box Plot)
    fig = px.box(
        df_box, 
        x='ccaa', 
        y='ia14', 
        title='Dispersión de la IA14 (Todos los días) por Comunidad Autónoma',
        labels={'ccaa': 'Comunidad Autónoma', 'ia14': 'IA14 (Casos/100k hab.)'},
        color='ccaa', # Colorea cada caja por CCAA
        template='plotly_white'
    )

    # 3. Mejora estética (Opcional, pero recomendable en Plotly)
    fig.update_layout(showlegend=False) # No necesitamos leyenda si el color es la CCAA
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig, width='stretch')
    
    # --- Demostración de .melt() usando datos de prueba si fuera necesario ---
    st.markdown("---")
    st.subheader("Demostración conceptual de `pd.melt()`")
    st.markdown(
        """
        Para este *Box Plot*, no fue necesario usar `pd.melt()` porque el DataFrame ya tiene la IA14 y la CCAA en **formato largo**.
        `pd.melt()` es indispensable cuando tenemos métricas en **formato ancho** (ej. `casos_pcr`, `casos_test_ac`) que queremos comparar:
        """
    )
    
    # Creamos un pequeño ejemplo de MELT para demostrar el dominio de la función
    if not df.empty and all(col in df.columns for col in ['date', 'ccaa', 'num_casos_prueba_pcr', 'num_casos_prueba_test_ac']):
        
        df_melt_ejemplo = df.groupby(['date', 'ccaa'])[['num_casos_prueba_pcr', 'num_casos_prueba_test_ac']].sum().reset_index()

        # [Dominio Pandas: Uso de .melt()]
        df_long = df_melt_ejemplo.melt(
            id_vars=['date', 'ccaa'], 
            value_vars=['num_casos_prueba_pcr', 'num_casos_prueba_test_ac'], 
            var_name='Tipo de Prueba', 
            value_name='Número de Casos'
        )
        
        if not df_long.empty:
            st.caption("Resultado de pd.melt() (Formato Largo para Composición)")
        
            st.dataframe(
                    df_long.head(10), # Usamos head(10) para una muestra más representativa
                    width='stretch' # Argumento común para ocupar todo el ancho
                )
            fig_melt = px.area(
                    df_long.head(50), 
                    x='date', 
                    y='Número de Casos', 
                    color='Tipo de Prueba',
                    title='Casos por Tipo de Prueba (Formato Largo)',
                    template='plotly_white'
                )
            st.plotly_chart(fig_melt, width='stretch')
                
        else:
            st.info("El DataFrame final (`df_long`) resultante de `pd.melt()` está vacío.")
# =========================================================================
# FLUJO PRINCIPAL DE 2_Análisis.py
# =========================================================================

st.title("🔬 Análisis Comparativo")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]

    st.markdown("---")
    
    analisis_comparativo_boxplot(df)
    
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")