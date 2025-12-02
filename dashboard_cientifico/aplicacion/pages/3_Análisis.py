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


# =========================================================================
# FLUJO PRINCIPAL (Controlador)
# =========================================================================


configura_streamlit()
st.title("🔬 Análisis Detallado de Datos")

if CLAVE_DATAFRAME in st.session_state and not st.session_state[CLAVE_DATAFRAME].empty:
    df: pd.DataFrame = st.session_state[CLAVE_DATAFRAME]
    lista_meses_cargados(df)
       
    tab1, tab2, tab3, tab4 = st.tabs(['Evolución', 'Evolución Mensual', 'Análisis Geográfico', 'Distribución'])

    with tab1:
        tab_titles = list(METRICAS_ANALISIS.values())
        tabs = st.tabs(tab_titles)
        
        for i, (col_key, tab_title) in enumerate(METRICAS_ANALISIS.items()):
            with tabs[i]:
                try:
                    df_evolucion = obtener_evolucion_mensual(df, col_key)
                    
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
        st.header("Análisis de Distribución Mensual")
        st.info("Este análisis muestra la dispersión, mediana y valores atípicos (outliers) de los totales mensuales de cada métrica.")
        
        # Reutilizamos las pestañas de métricas
        tab_titles_distribucion = list(METRICAS_ANALISIS.values())
        tabs_distribucion = st.tabs(tab_titles_distribucion) 
        
        # Iterar sobre las métricas
        for i, (col_key, tab_title) in enumerate(METRICAS_ANALISIS.items()):
            
            with tabs_distribucion[i]: 
                try:
                    st.subheader(f'Distribución de {tab_title}')
                    
                    # 1. LLAMADA AL MODELO: Reutilizamos df_evolucion
                    # Los datos ya están agrupados por mes, listos para la distribución
                    df_evolucion = obtener_evolucion_mensual(df, col_key)

                    # 2. LLAMADA A LA VISTA (Gráfico de Caja)
                    grafico_distribucion(df, col_key, tab_title)
                    
                    # Opcional: Mostrar estadísticas descriptivas (Media, Mediana, etc.)
                    df_evolucion = obtener_evolucion_mensual(df, col_key)
                    st.markdown("**Estadísticas Descriptivas (Totales Mensuales):**")
                    st.dataframe(df_evolucion[col_key].describe().round(2), width='stretch')
                    
                except Exception as e:
                    st.error(f"No hay datos para generar el análisis de distribución para {tab_title}.")

    with tab4:
        st.header("Análisis de Correlación Mensual")
        st.info("Muestra la correlación de Pearson entre los totales mensuales de las métricas.")
        
        # Lista de claves (columnas) a correlacionar
        metricas_claves = list(METRICAS_ANALISIS.keys())
        
        try:
            # 1. LLAMADA AL MODELO: Obtener Matriz de Correlación
            matriz_corr = obtener_matriz_correlacion_mensual(df, metricas_claves)
            
            # 2. LLAMADA A LA VISTA (Mapa de Calor)
            grafico_correlacion(matriz_corr, METRICAS_ANALISIS)
            
            # 3. Mostrar Datos (Matriz)
            with st.expander("Datos de la Matriz de Correlación", expanded=False):
                st.dataframe(matriz_corr, width='stretch')
                
        except Exception as e:
            st.error(f"No fue posible calcular la matriz de correlación. Error: {e}")
else:
    st.warning("Datos no disponibles. Por favor, asegúrate de que la Carga Inicial se ha completado en la página 'Inicio'.")
