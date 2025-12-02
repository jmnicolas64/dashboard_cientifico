import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard_cientifico.aplicacion.config.settings import CLAVE_DATAFRAME
from dashboard_cientifico.aplicacion.config.config_streamlit import configura_streamlit

from dashboard_cientifico.aplicacion.modelo.funciones_graficos import (obtener_evolucion_mensual,
                                                                       obtener_matriz_correlacion_mensual)

from dashboard_cientifico.aplicacion.vista.vista import (lista_meses_cargados,
                                                         grafico_evolucion_mensual,
                                                         grafico_distribucion,
                                                         grafico_correlacion)

METRICAS_ANALISIS = {
    "num_def": "Defunciones",
    "new_cases": "Casos",
    "num_hosp": "Hospitalizados",
    "num_uci": "UCI"
}


configura_streamlit()
st.header("Análisis Detallado de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
    
    if not df.empty and pd.api.types.is_datetime64_any_dtype(df['date']):   
        fecha_minima = df['date'].min().date()
        fecha_maxima = df['date'].max().date()
        
        st.sidebar.markdown("#### Filtrado temporal")
        
        rango_fechas = st.sidebar.slider(
            'Selecciona el Rango de Fechas:',
            min_value=fecha_minima,
            max_value=fecha_maxima,
            value=(fecha_minima, fecha_maxima),
            format="DD/MM/YYYY"
        )
        
        fecha_inicio_seleccionada = pd.to_datetime(rango_fechas[0])
        fecha_fin_seleccionada = pd.to_datetime(rango_fechas[1])
        
        df_filtrado = df[
            (df['date'] >= fecha_inicio_seleccionada) & 
            (df['date'] <= fecha_fin_seleccionada)
        ].copy()  
    else:
        st.warning("El DataFrame no está disponible o la columna 'date' no es de tipo fecha.")
        df_filtrado = df.copy()

    tab1, tab2, tab3, tab4 = st.tabs(['Evolución', 'Distribución', 'Análisis Geográfico', 'Correlación'])

    with tab1:
        st.subheader("Evolución Mensual")
        st.info("Este análisis muestra la evolución mensual de cada métrica.")        
        
        tab_titles = list(METRICAS_ANALISIS.values())
        tabs = st.tabs(tab_titles)
        
        for i, (col_key, tab_title) in enumerate(METRICAS_ANALISIS.items()):
            with tabs[i]:
                try:
                    df_evolucion = obtener_evolucion_mensual(df_filtrado, col_key)
                    
                    grafico_evolucion_mensual(
                        df_evolucion, 
                        col_key,
                        tab_title
                    )

                    df_presentacion = df_evolucion.copy()
                    df_presentacion['date'] = df_presentacion['date'].dt.strftime('%m/%Y') # type: ignore
                    df_presentacion.rename(columns={'date': 'Fecha',
                                                    col_key: tab_title
                                                    }, inplace=True)

                    with st.expander("Datos del gráfico", expanded=False):
                        st.dataframe(df_presentacion, width='stretch')

                except Exception as e:
                    st.error("No hay datos para generar el análisis de evolución para " + tab_title + ".")

    with tab2:
        st.subheader("Análisis de Distribución")
        st.info("Este análisis muestra la dispersión, mediana y valores atípicos de los totales mensuales de cada métrica.")
        
        tab_titles_distribucion = list(METRICAS_ANALISIS.values())
        tabs_distribucion = st.tabs(tab_titles_distribucion) 
        
        for i, (col_key, tab_title) in enumerate(METRICAS_ANALISIS.items()):
            
            with tabs_distribucion[i]: 
                try:
                    st.subheader(f'Distribución de {tab_title}')

                    df_evolucion = obtener_evolucion_mensual(df_filtrado, col_key)

                    grafico_distribucion(df_filtrado, col_key, tab_title)
                    
                    st.markdown("**Estadísticas Descriptivas (Totales Mensuales):**")
                    st.dataframe(df_evolucion[col_key].describe().round(2), width='stretch')
                    
                except Exception as e:
                    st.error(f"No hay datos para generar el análisis de distribución para {tab_title}.")

    with tab4:
        st.subheader("Análisis de Correlación Mensual")
        st.info("Muestra la correlación de Pearson entre los totales mensuales de las métricas.")
        
        metricas_claves = list(METRICAS_ANALISIS.keys())
        
        try:
            matriz_corr = obtener_matriz_correlacion_mensual(df_filtrado, metricas_claves)
            grafico_correlacion(matriz_corr, METRICAS_ANALISIS)

            with st.expander("Datos de la Matriz de Correlación", expanded=True):
                st.dataframe(matriz_corr, width='stretch')
                
        except Exception as e:
            st.error(f"No fue posible calcular la matriz de correlación. Error: {e}")
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")
