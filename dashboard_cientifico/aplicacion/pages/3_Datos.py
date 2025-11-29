# C:\...\aplicacion\pages\3_Datos.py

import streamlit as st
import pandas as pd
import numpy as np

from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit


def generar_ranking_formateado(df: pd.DataFrame):
    """
    Genera y muestra un ranking de CCAA por IA14 con formato condicional de Pandas Styler.
    Demuestra el dominio de Pandas para la presentación de datos.
    """
    st.subheader("Ranking de Incidencia Acumulada (IA14) Formateado")
    st.markdown("_(Demostrando **formato condicional** y manejo de **índices** con Pandas Styler)_")

    # 1. Preparación de Datos: Ranking (Dominio de Pandas)
    
    # a) Encontrar el último día disponible
    ultimo_dia = df['date'].max()
    df_ultimo_dia = df[df['date'] == ultimo_dia]
    
    # b) Agrupar por CCAA y calcular las métricas
    df_ranking = df_ultimo_dia.groupby('ccaa').agg(
        IA14_Promedio=('ia14', 'mean'), 
        Casos_Totales=('cases_accumulated', 'sum'),
        Poblacion=('poblacion', 'mean')
    ).reset_index()

    # Calcular la IA14 Nacional (para el formato condicional)
    ia14_nacional = df_ranking['IA14_Promedio'].mean()

    # Ordenar y preparar el Ranking
    df_ranking = df_ranking.sort_values(by='IA14_Promedio', ascending=False).reset_index(drop=True)
    df_ranking.index = df_ranking.index + 1 # Empezar el índice en 1 para el ranking
    
    # Añadir la columna de Ranking (ahora es una columna normal, no el índice de Pandas)
    df_ranking.insert(0, 'Ranking', df_ranking.index) # Inserta la columna 'Ranking' al principio
    df_ranking.reset_index(drop=True, inplace=True) 

    # 2. Formato Condicional (Dominio de Pandas Styler)
    
    # Definir el styler para aplicar formatos
    styler = (
        df_ranking.style
        .format({
            'IA14_Promedio': "{:.2f}", # Dos decimales
            'Casos_Totales': "{:,.0f}",  # Separador de miles sin decimales
            'Poblacion': "{:,.0f}" # Separador de miles sin decimales
        })
        .hide(axis="index") # Oculta el índice de Pandas, que ahora es superfluo
        .set_caption(f"Ranking de CCAA al último día: {ultimo_dia.strftime('%Y-%m-%d')}")
        
        # Aplicación Corregida: Usamos axis=0 (columna por columna)
        .apply(
            lambda s: [
                'background-color: #F5B7B1' if v > ia14_nacional else '' 
                for v in s 
            ], 
            axis=0, 
            subset=['IA14_Promedio']
        )
        
        # Opcional: Resaltar el máximo (la celda con el valor más alto)
        .highlight_max(subset=['IA14_Promedio'], color='red')
    )
    
    # 3. Presentación
    st.markdown(f"**Media Nacional de IA14:** `{ia14_nacional:.2f}` (Las filas con fondo rojo superan esta media)")
    
    # Pasamos el objeto styler directamente a st.dataframe.
    st.dataframe(styler, width='stretch')

# =========================================================================
# FLUJO PRINCIPAL DE 3_Datos.py
# =========================================================================


configura_streamlit()
st.title("🗃️ Presentación de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]

    st.markdown("---")
    
    generar_ranking_formateado(df)
    
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")